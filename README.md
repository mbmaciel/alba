Tornar executável:

$ python .\setup.py build

No Windows, distribua a pasta gerada inteira, não apenas o arquivo `.exe`.
No workflow do GitHub Actions, o artefato é publicado como um `.zip` justamente
para preservar todos os arquivos que o executável precisa para abrir.

## Execução no macOS

No macOS, use um Python com Tk fora do Xcode. A combinação validada neste
projeto foi:

```bash
brew install tcl-tk python-tk@3.13
/opt/homebrew/bin/python3.13 -m venv .venv-macos
./.venv-macos/bin/python -m pip install -r requirements.txt
./run-macos.sh
```


## Configuração do banco de dados

O caminho para o arquivo SQLite pode ser especificado através da variável de
ambiente `ALBA_DB_PATH`. Caso não seja definido, o aplicativo utiliza o caminho
`database/alba.db`.

Exemplo de execução com um caminho customizado:

```bash
export ALBA_DB_PATH=/caminho/para/alba.db
python main.py
```
