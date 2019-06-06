# lang-stats
Collect personal programming language statistics from GitHub repos using [PyGithub](https://pygithub.readthedocs.io/en/latest/).

This project is now archived and the functionality has been merged into my [meta-repository](https://github.com/kelly-sovacool/meta-repo).

## Usage

1. Clone this repo.

    ```
    git clone https://github.com/kelly-sovacool/lang-stats
    ```

1. Create a file `credentials.yaml` with your github login info:

    ```
    login: your_login
    password: your_password
    ```

    **Warning**: do not add the credentials file to git. Be careful not to accidentally share it with anyone.

1. Install dependencies:

    ```
    conda env create -n lang-stats -f environment.simple.yaml
    conda activate lang-stats
    ```

1. Create plots of your programming languages from your github repos:

    ```
    ./langstats.py
    ```

    They will be located in `figures/`.

    ![language_all_bytes](figures/language_all_bytes.svg)

    ![language_top_repos](figures/language_top_repos.svg)

## Notes

Jupyter is way over-represented because `.ipynb` files are JSON with lots of metadata.
- It'd be cool to parse out the code chunks and only let code count towards the byte count.
- Does linguist count comments in regular text files (e.g. `.py` or `.R`) towards the code byte count?
- Try counting bytes in regular `.py` files to make sure my method matches that of linguist, then apply it to Jupyter code chunks stripped of metadata.
