import argparse
import json
from pathlib import Path
from datetime import datetime

ITEMS_FILE = Path('items.json')


def load_items():
    if ITEMS_FILE.exists():
        with open(ITEMS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_items(items):
    with open(ITEMS_FILE, 'w', encoding='utf-8') as f:
        json.dump(items, f, indent=2, ensure_ascii=False)


def add_item(name, price, quantity):
    items = load_items()
    item_id = 1 if not items else items[-1]['id'] + 1
    item = {'id': item_id, 'name': name, 'price': price, 'quantity': quantity}
    items.append(item)
    save_items(items)
    print(f"Item cadastrado: {item}")


def list_items():
    items = load_items()
    if not items:
        print('Nenhum item cadastrado.')
        return
    for item in items:
        print("ID: {} | Nome: {} | Preço: {} | Quantidade: {}".format(item["id"], item["name"], item["price"], item["quantity"]))


def issue_invoice(ids):
    items = load_items()
    selected = [item for item in items if item['id'] in ids]
    if not selected:
        print('Nenhum item encontrado para os IDs fornecidos.')
        return
    total = sum(item['price'] * item['quantity'] for item in selected)
    invoice_number = int(datetime.now().timestamp())
    filename = f'invoice_{invoice_number}.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('Nota Fiscal\n')
        f.write(f'Numero: {invoice_number}\n')
        f.write(f'Data: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n\n')
        for item in selected:
            line = "{} - {} x {} = {}\n".format(
                item["name"], item["quantity"], item["price"], item["quantity"] * item["price"]
            )
            f.write(line)
        f.write(f"\nTotal: {total}\n")
    print(f'Nota fiscal gerada em {filename}')


def parse_args():
    parser = argparse.ArgumentParser(description='Sistema de cadastro de itens e emissao de nota fiscal')
    sub = parser.add_subparsers(dest='command')

    add = sub.add_parser('add', help='Cadastrar novo item')
    add.add_argument('--name', required=True)
    add.add_argument('--price', type=float, required=True)
    add.add_argument('--quantity', type=int, required=True)

    sub.add_parser('list', help='Listar itens cadastrados')

    invoice = sub.add_parser('invoice', help='Emitir nota fiscal')
    invoice.add_argument('--ids', required=True, help='IDs de itens separados por virgula')

    return parser.parse_args()


def main():
    args = parse_args()
    if args.command == 'add':
        add_item(args.name, args.price, args.quantity)
    elif args.command == 'list':
        list_items()
    elif args.command == 'invoice':
        ids = [int(i) for i in args.ids.split(',') if i.strip().isdigit()]
        issue_invoice(ids)
    else:
        print('Comando invalido. Use --help para detalhes.')


if __name__ == '__main__':
    main()
