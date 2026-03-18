import os
import sqlite3

DEFAULT_DB_PATH = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "database", "alba.db")
)
DB_PATH = os.environ.get("ALBA_DB_PATH", DEFAULT_DB_PATH)

WORD_REPLACEMENTS = {
    "DEPaSITO": "DEPÓSITO",
    "SIMBaLICO": " SIMBÓLICO",
    "T+TULO": "TÍTULO",
    "TEMPORÃRIA": "TEMPORÁRIA",
    "ÃREAS": "ÁREAS",
    "ATRIBU+DA": "ATRIBUÍDA",
    "ORIGINÃRIO": "ORIGINÁRIO",
    "TRIBUTÃRIA": "TRIBUTÁRIA",
    "DESTINATÃRIO": "DESTINATÁRIO",
    "USUÃRIO": "USUÁRIO",
    "GRÂTIS": "GRÁTIS",
    "SIMBaLICA": "SIMBÓLICA",
    "DEMONSTRAÇ¦O": "DEMONSTRAÇÃO",
    "S¦O PAULO": "SÃO PAULO",
    "MANUTENÇ¦O": "MANUTENÇÃO",
    "RAZ¦O": "RAZÃO",
    "M¦XIMO": "MÁXIMO",
    "DEVOLUÇ¦O": "DEVOLUÇÃO",
    "SA+DA": "SAÍDA",
    "CONDIÇ¦O": "CONDIÇÃO",
    "SUBSTITUIÇ¦O": "SUBSTITUIÇÃO",
    "TRIBUT¦RIA": "TRIBUTÁRIA",
    "VALIDAÇ¦O": "VALIDAÇÃO",
    "INSTRUÇ¦O": "INSTRUÇÃO",
    "INFORMAÇ¦O": "INFORMAÇÃO",
    "DEVER¦O": "DEVERÃO",
    "ESPEC+FICO": "ESPECÍFICO",
    "TRIBUT¦RIO": "TRIBUTÁRIO",
    "J¦": "JÁ",
    "GR|O": "GRÃO",
    "ALGOD¦O": "ALGODÃO",
    "C¦RTAMO": "CÔRTAMO",
    "R+CINIO ": "RÓCINIO ",
    "MEL¦O": "MELÃO",
    "RA+ZES": "RAÍZES", 
    "CHICaRIA": "CHICORIA",
    "POSIÇ¦O": "POSIÇÃO",
    "COMBUST+VEL": "COMBUSTÍVEL",
    "TRANSFER-NCIA": "TRANSFERÊNCIA",
    "GRÃTIS": "GRÁTIS",
    "JÃ": "JÁ",
    "DEMONSTRACAO": "DEMONSTRAÇÃO",
    "AGROINDTSTRIA": "AGROINDÚSTRIA",
    "AUTGNOMO": "AUTÔNOMO",
    "ESTÃ": "ESTÁ",
    "SAIDAS": "SAÍDAS",
    "SERVICO": "SERVIÇO",
    "DECORR-NCIA": "DECORRÊNCIA",
    "+": "À",
    "V¦LIDAS": "VÁLIDAS",
    "TRANSAÇ¦O": "TRANSAÇÃO",
    "COTAÇ¦O": "COTAÇÃO",
    "MÀNIMO": "MÍNIMO",
    "CONDIÇsES": "CONDIÇÕES",
    "SOLICITAÇsES": "SOLICITAÇÕES",
    "PRaPRIO": "PRÓPRIO",
    "N¦O": "NÃO",


}


def robust_text_factory(data):
    if isinstance(data, bytes):
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError:
            return data.decode("latin1")
    return data


def apply_replacements(value):
    """
    Corrige problemas de codificação e substitui palavras corrompidas.
    """
    if not value:
        return value

    fixed_value = value

    if "СЕҐ%" in fixed_value:
        fixed_value = fixed_value.replace("|", "З?")

    for wrong, right in WORD_REPLACEMENTS.items():
        if wrong in fixed_value:
            fixed_value = fixed_value.replace(wrong, right)

    return fixed_value


def fix_table(cursor, table_name, code_column, name_column):
    """
    Procura problemas de encoding e palavras corrompidas e corrige o nome.
    """
    print(f"\n--- Checking for encoding issues in '{table_name}' ---")
    cursor.execute(f"SELECT {code_column}, {name_column} FROM {table_name}")
    rows = cursor.fetchall()

    updated_count = 0
    for code_value, name_value in rows:
        new_name_value = apply_replacements(name_value)
        if new_name_value != name_value:
            print(
                f"Updating {table_name.upper()} {code_value}: "
                f"'{name_value}' -> '{new_name_value}'"
            )
            cursor.execute(
                f"UPDATE {table_name} SET {name_column} = ? WHERE {code_column} = ?",
                (new_name_value, code_value),
            )
            updated_count += 1

    if updated_count > 0:
        print(f"Success! Updated {updated_count} records in {table_name}.")
    else:
        print(f"No records found needing update in {table_name}.")
    return updated_count


def fix_textos(cursor):
    """
    Aplica as correções em todos os campos textuais da tabela TEXTOS.
    """
    columns = ["NM_DESCRICAO", "TX_PRAZO", "TX_CONDICOES", "TX_OBS"]
    print("\n--- Checking for encoding issues in 'TEXTOS' ---")
    cursor.execute(f"SELECT RECNUM, {', '.join(columns)} FROM TEXTOS")
    rows = cursor.fetchall()

    updated_count = 0
    for row in rows:
        recnum, *values = row
        new_values = [apply_replacements(value) for value in values]
        if new_values != list(values):
            changed_cols = [col for col, old, new in zip(columns, values, new_values) if new != old]
            print(f"Updating TEXTOS {recnum} columns {', '.join(changed_cols)}")
            assignments = ", ".join(f"{col} = ?" for col in columns)
            cursor.execute(
                f"UPDATE TEXTOS SET {assignments} WHERE RECNUM = ?",
                (*new_values, recnum),
            )
            updated_count += 1

    if updated_count > 0:
        print(f"Success! Updated {updated_count} records in TEXTOS.")
    else:
        print("No records found needing update in TEXTOS.")
    return updated_count


def fix_encoding():
    print(f"Connecting to {DB_PATH}")
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.text_factory = robust_text_factory
        cursor = conn.cursor()

        total_updates = 0
        total_updates += fix_table(cursor, "cfop", "cd_cfop", "nm_cfop")
        total_updates += fix_table(cursor, "ncm", "cd_ncm", "nm_ncm")
        total_updates += fix_table(cursor, "natop", "id_natop", "ds_natop")
        total_updates += fix_table(cursor, "alba0008", "id_of", "tx_obs")
        total_updates += fix_textos(cursor)

        if total_updates > 0:
            conn.commit()
            print(f"\nAll done! Updated {total_updates} records in total.")
        else:
            print("\nNo records needed updates.")

        conn.close()

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    fix_encoding()
