# Python Discord Summer Code Jam 21'
## Team Grand Geckos presents.. SECRET CRATE OF GRAND GECKOS
<p align=center><img src="https://github.com/imsofi/codejam-grand-geckos/raw/develop/assets/images/grand_gecko_logo@0.5x.png" alt="Team Grand Geckos' Logo By Nikz Jon(nikhiljohn10)" width="500"/></p>

[About Python Discord's Code Jam 8](https://pythondiscord.com/events/code-jams/8/)

## About the project...

As the name indicates, our project is a very secret and mostly safe crate... of course.. it's a **TUI** password manager!

Our password manager stores your data locally, encrypted in a `Vault` inside that crate.. that can be only unlocked by.. *YOU*!

You can add credentials as you wish, but if you don't want to bother with creating safe passwords.. just leave it to us, we'll do it.
But, you can also store your pre-existing credentials as well, it'll be safely stored in the Vault.


## How to setup the project?

* *Requires Python 3.8 or higher*

* *The project also uses SQLite 3*
### Dependency:
  * Poetry
  ```bash
  pip install --user poetry
  ```

### First Time Setup:

```bash
git clone https://github.com/imsofi/codejam-grand-geckos
cd codejam-grand-geckos
poetry install
poetry run pre-commit install
```

### Running the Project:

* Using `poetry run`:
  ```bash
  poetry run task main
  ```

* If you are in a `poetry shell`:
  ```bash
  python3 -m grand_geckos
  ```

### Note

It' s reccomended to run the code trough the linters manually:

* With `poetry run` command:
  ```bash
  poetry run task lint
  ```

* Or run it trough `poetry shell`:
  ```bash
  pre-commit run --all-files
  ```

If you get errors while running `poetry install`. Try following command:
  ```bash
  poetry update
  ```
