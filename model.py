from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, DataCollatorWithPadding, get_scheduler
from datasets import load_dataset
from torch.utils.data import DataLoader
from torch.optim import AdamW
from accelerate.test_utils.testing import get_backend
from tqdm.auto import tqdm
from torch.amp import autocast, GradScaler

import torch
# import evaluate

model_name = "google/flan-t5-large"
batch_size = 1

scaler = GradScaler()

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

raw_dataset = load_dataset("csv", data_files={"full": "/kaggle/input/games-data/games_data.csv"})["full"]
# print("Raw dataset features:", raw_dataset.features)

split_dataset = raw_dataset.train_test_split(test_size=0.2, seed=42)
# print(split_dataset)
def tokenize_function(examples):
    # inputs = tokenizer(examples["inputs"], truncation=True, padding="max_length", max_length=512)
    # labels = tokenizer(examples["label"], truncation=True, padding="max_length", max_length=512)
    inputs = tokenizer(examples["inputs"], truncation=False, padding=True)
    labels = tokenizer(examples["label"], truncation=False, padding=True)

    inputs["labels"] = labels["input_ids"]
    return inputs

tokenized_dataset = split_dataset.map(tokenize_function, batched=True)
# Potentially remove inputs col
tokenized_dataset = tokenized_dataset.remove_columns(["inputs", "label"])
# tokenized_dataset = tokenized_dataset.remove_columns(["inputs"])
# tokenized_dataset = tokenized_dataset.rename_column("label", "labels")
tokenized_dataset.set_format("torch")
print(tokenized_dataset)

data_collator = DataCollatorWithPadding(tokenizer)

train_dataloader = DataLoader(tokenized_dataset["train"], shuffle=True, batch_size=batch_size, collate_fn=data_collator)
eval_dataloader = DataLoader(tokenized_dataset["test"], batch_size=batch_size, collate_fn=data_collator)

optimizer = AdamW(model.parameters(), lr=5e-5)

num_epochs = 3
num_training_steps = num_epochs * len(train_dataloader)
lr_scheduler = get_scheduler(
    name="linear", optimizer=optimizer, num_warmup_steps=0, num_training_steps=num_training_steps
) # Used to adjust the learning rate of the optimizer during training

device, _, _ = get_backend() # automatically detects the underlying device type (CUDA, CPU, XPU, MPS, etc.)
model.to(device)

progress_bar = tqdm(range(num_training_steps))

# Train
model.train()
for epoch in range(num_epochs):
    for batch in train_dataloader:
        batch = {k: v.to(device) for k, v in batch.items()}

        with autocast():
            outputs = model(**batch)
            loss = outputs.loss
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.step(lr_scheduler)
        optimizer.zero_grad()
        progress_bar.update(1)

# Evaluate
# metric = evaluate.load("accuracy")
model.eval()
predictions_text = []
for batch in eval_dataloader:
    batch = {k: v.to(device) for k, v in batch.items()}
    with torch.no_grad():
        outputs = model(**batch)

    logits = outputs.logits
    predictions = torch.argmax(logits, dim=-1)
    decoded_preds = tokenizer.batch_decode(predictions, skip_special_tokens=True)
    predictions_text.append(decoded_preds)
#     metric.add_batch(predictions=predictions, references=batch["labels"])

# metric.compute()
print(len(predictions_text[0]))
print(predictions_text[0])