# Pushing Large Files with Git LFS

Git LFS (Large File Storage) is needed when working with large files like datasets, models, and binaries.

## Setup Instructions

1. Install Git LFS
   ```bash
   # Windows (using Chocolatey)
   choco install git-lfs

   # macOS (using Homebrew)
   brew install git-lfs

   # Linux (using apt)
   sudo apt install git-lfs
   ```

2. Initialize Git LFS in your repository
   ```bash
   git lfs install
   ```

3. Track large file patterns
   ```bash
   # Track specific file extensions
   git lfs track "*.csv"
   git lfs track "*.pkl"
   git lfs track "*.pt"

   # Track specific files
   git lfs track "path/to/large/file.csv"
   ```

4. Commit the .gitattributes file
   ```bash
   git add .gitattributes
   git commit -m "Configure Git LFS tracking"
   ```

5. Use Git normally
   ```bash
   git add .
   git commit -m "Add large files"
   git push
   ```

## Common Issues

- **Push fails**: Ensure Git LFS is properly initialized
- **Files not tracking**: Check .gitattributes for correct patterns
- **Storage quota**: Monitor LFS storage usage on your Git provider

## Useful Commands

- Check tracked patterns: `git lfs track`
- List tracked files: `git lfs ls-files`
- Pull LFS files: `git lfs pull`
- Check LFS status: `git lfs status`

## References
- [Git LFS Documentation](https://git-lfs.com)
- [GitHub LFS Guide](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage)
- [Claude Conversation about Git LFS](https://claude.ai/share/5bf730d7-e1a6-4958-b9cb-9b9158b74ffe)
