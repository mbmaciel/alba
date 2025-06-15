Tornar executável:

$ pyinstaller --onefile --windowed main.py

## Configuração do banco de dados

O caminho para o arquivo SQLite pode ser especificado através da variável de
ambiente `ALBA_DB_PATH`. Caso não seja definido, o aplicativo utiliza o caminho
`alba_zip_extracted/alba.sqlite`.

Exemplo de execução com um caminho customizado:

```bash
export ALBA_DB_PATH=/caminho/para/alba.sqlite
python main.py
```
