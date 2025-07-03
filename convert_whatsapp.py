import sys
import re
from datetime import datetime

def convert_line(line):
    # Regex actualizado
    match = re.match(r'^(\d{1,2}/\d{1,2}/\d{2}), (\d{1,2}:\d{2}) - (.*?): (.*)$', line)
    if not match:
        return line
    
    date_str, time_str, user, message = match.groups()

    # Normalizar hora a formato HH:MM (añadir 0 si es hora de un dígito)
    if len(time_str.split(':')[0]) == 1:
        time_str = '0' + time_str

    dt = datetime.strptime(date_str + ' ' + time_str, '%d/%m/%y %H:%M')

    new_date_str = dt.strftime('[%d.%m.%y, %H:%M:%S]')

    new_line = f'{new_date_str} {user}: {message}'

    return new_line


def clean_line(line):
    # Eliminar caracteres de control excepto tab y salto de línea
    return ''.join(ch for ch in line if ch.isprintable() or ch in '\t\n\r')

def main():
    if len(sys.argv) != 3:
        print("Uso: python3 convertir_whatsapp.py archivo_entrada.txt archivo_salida.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    last_was_multimedia = False

    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(output_file, 'w', encoding='utf-8') as f_out:
        for line in f_in:
            line = line.rstrip('\n')
            line = clean_line(line)

            if line.strip() == "":
                continue

            if "<Multimedia omitido>" in line:
                if last_was_multimedia:
                    continue  # saltar líneas repetidas consecutivas
                else:
                    last_was_multimedia = True
            else:
                last_was_multimedia = False


            converted = convert_line(line)
            f_out.write(converted + '\n')

    print(f'Archivo convertido guardado en {output_file}')

if __name__ == '__main__':
    main()
