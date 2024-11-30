# gitcommit
## AI-Generated Git Commit Messages

**gitcommit** is a command-line tool that uses OpenAI's GPT models to generate concise and properly formatted Git commit messages based on staged changes. It simplifies the process of creating meaningful commit messages, ensuring consistency and clarity in your Git history.

## Features
- Automatically generates commit messages based on `git diff` output.
- Supports a test mode for previewing the commit message.
- User confirmation before committing changes.

## Installation

### Prerequisites
1. **Python 3.9 or higher**: Ensure Python is installed on your system. You can check your Python version with:
   ```bash
   python3 --version
   ```

2. **Git**: Make sure Git is installed. You can check by running:
   ```bash
   git --version
   ```

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/jeffreality/gitcommit.git
   cd gitcommit
   ```

2. Run the setup script:
   ```bash
   python3 setup.py
   ```

   The script will:
   - Prompt you for your OpenAI API key (see below for obtaining the key).
   - Create a virtual environment.
   - Install required dependencies.
   - Install the `gitcommit` command globally.

3. Obtain an OpenAI API key:
   - Sign up or log in to OpenAI at [https://platform.openai.com/](https://platform.openai.com/).
   - Navigate to the API section and generate a new API key.
   - Paste the key when prompted during the setup process.

## Usage

1. Stage your changes using Git:
   ```bash
   git add <file>
   ```

2. Run `gitcommit` to generate a commit message and apply it:
   ```bash
   gitcommit
   ```

   - You'll see the generated commit message and be prompted to confirm the commit.
   - To preview the message without committing, use:
     ```bash
     gitcommit --test
     ```

3. After confirming the commit, you can push your changes:
   ```bash
   git push
   ```

## Future Enhancements

The following are some ideas for future enhancement:
- **Command-line options**:
  - Specify a custom maximum number of tokens for message generation (to override the default).
  - Customize the GPT model dynamically.
- **Automatic Git push**: Add an option to automatically push commits after confirmation.
- **Enhanced support for other operating systems**: Add detailed setup instructions for Linux and Windows.
- **Customizable message templates**: Allow users to provide templates for commit message formats.
- **Support for other LLMs**: Expand to use additional LLMs like Claude or Gemini for commit suggestions.

## Contributing

Contributions are welcome! If you have ideas for enhancements, bug fixes, or additional features, feel free to:
1. Fork this repository.
2. Create a new branch for your feature or fix.
3. Submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Support

If you encounter any issues, please open an issue in the [GitHub Issues](https://github.com/jeffreality/gitcommit/issues) section.