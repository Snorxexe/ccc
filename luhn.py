import random

def luhn_checksum(num_str):
    digits = [int(d) for d in num_str]
    for i in range(len(digits)-2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    return sum(digits) % 10

def generate_luhn(bin_num, count, exp_date=None):
    cards = []

    for _ in range(count):
        base = bin_num
        while len(base) < 15:
            base += str(random.randint(0, 9))

        checksum = luhn_checksum(base)
        check_digit = (10 - checksum) % 10

        full_card = base + str(check_digit)

        # Exp date
        if exp_date:
            month, year = exp_date
        else:
            month = str(random.randint(1, 12)).zfill(2)
            year = str(random.randint(2025, 2030))

        cvv = "000"

        cards.append(f"{full_card}|{month}|{year}|{cvv}")

    return cards


if __name__ == "__main__":
    bin_num = input("BIN gir (6-8 haneli): ").strip()
    adet = int(input("Kaç kart üretilecek: "))

    tarih = input("Tarih gir (MM|YYYY) boş bırakırsan rastgele: ").strip()

    if tarih:
        mm, yy = tarih.split("|")
        exp = (mm, yy)
    else:
        exp = None

    result = generate_luhn(bin_num, adet, exp)

    print("\n--- Üretilen TEST Kartları ---")
    for r in result:
        print(r)
