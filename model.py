from transformers import AutoTokenizer, AutoModelForCausalLM, DataCollatorWithPadding, get_scheduler
from datasets import load_dataset
from torch.utils.data import DataLoader
from torch.optim import AdamW
from accelerate.test_utils.testing import get_backend
from tqdm.auto import tqdm

import torch

# TODO add validation set

# Adjustable variables
model_name = "google/gemma-2-2b"
batch_size = 1
train_dataset_path = "/content/train_dataset.csv"
test_dataset_path = "/content/test_dataset.csv"
num_epochs = 10
learning_rate = 1e-5
model_dir = f"{model_name}_saved"

# "google/flan-t5-base"

# model_config = {"rope_scaling": {"type": "linear", "factor": 8.0}}

tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(model_name, config=model_config)
model = AutoModelForCausalLM.from_pretrained(model_name)
model.gradient_checkpointing_enable()
model.half()


# Load datasets in streaming mode
train_dataset = load_dataset("csv", data_files={"full": train_dataset_path}, streaming=True)["full"]
eval_dataset = load_dataset("csv", data_files={"full": test_dataset_path}, streaming=True)["full"]

# Tokenize dynamically using a collate function
tokenizer.add_special_tokens({'pad_token': '[PAD]'})
model.resize_token_embeddings(len(tokenizer))
def tokenize_batch(batch):
    inputs_text = [example["inputs"] for example in batch]
    labels_text = [example["label"] for example in batch]

    # inputs = tokenizer(inputs_text, truncation=True, padding=True, max_length=512, return_tensors="pt")
    # labels = tokenizer(labels_text, truncation=True, padding=True, max_length=512, return_tensors="pt")
    inputs = tokenizer(
        inputs_text,
        truncation=False,
        padding="max_length",
        max_length=256,
        return_tensors="pt",
        add_special_tokens=True,
        )
    labels = tokenizer(
        labels_text,
        truncation=False,
        padding="max_length",
        max_length=256,
        return_tensors="pt",
        add_special_tokens=True,
        )

    inputs["labels"] = labels["input_ids"]
    return inputs

# DataLoaders
train_dataloader = DataLoader(train_dataset, batch_size=batch_size, collate_fn=tokenize_batch)
eval_dataloader = DataLoader(eval_dataset, batch_size=batch_size, collate_fn=tokenize_batch)

optimizer = AdamW(model.parameters(), lr=learning_rate)

# Scheduler (num_training_steps calculated dynamically)
lr_scheduler = get_scheduler(
    name="linear", optimizer=optimizer, num_warmup_steps=0, num_training_steps=1  # Placeholder
)

# Device setup
device, _, _ = get_backend()
print(f"Using device: {device}")
model.to(device)

# Train
progress_bar = tqdm(total=None)  # Dynamic progress bar
model.train()
step_count = 0  # Manually count steps

for epoch in range(num_epochs):
    print(f"Epoch: {epoch + 1}/{num_epochs}")
    for batch in train_dataloader:
        batch = {k: v.to(device) for k, v in batch.items()}

        outputs = model(**batch)
        loss = outputs.loss
        loss.backward()

        optimizer.step()
        lr_scheduler.step()
        optimizer.zero_grad()
        progress_bar.update(1)

        step_count += 1  # Increment step count

progress_bar.close()

# Update lr_scheduler with actual training steps
lr_scheduler = get_scheduler(
    name="linear", optimizer=optimizer, num_warmup_steps=0, num_training_steps=step_count
)

# Evaluate
model.eval()
predictions_text = []
for batch in eval_dataloader:
    print("Input shape:", batch["input_ids"].shape)
    print("Labels shape:", batch["labels"].shape)
    batch = {k: v.to(device) for k, v in batch.items()}
    with torch.no_grad():
        outputs = model(**batch)

    # Use model.generate for predicti   ons
    generated_ids = model.generate(input_ids=batch["input_ids"], max_length=512)
    # generated_ids = model.generate(input_ids=batch["input_ids"])

    decoded_preds = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
    predictions_text.extend(decoded_preds)

print(len(predictions_text))
print(predictions_text)

model.save_pretrained(model_dir)  # Save model
tokenizer.save_pretrained(model_dir)  # Save tokenizer

print(f"Model and tokenizer saved to {model_dir}")
