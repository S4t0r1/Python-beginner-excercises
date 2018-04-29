
alphabet = "abcdefghijklmnopqrstuvwxyz"
en_ics_lst = [0.0815, 0.0144, 0.0276, 0.0379, 0.1311, 0.0292, 0.0199, 0.0526, 0.0635, 
             0.0013, 0.0042, 0.0339, 0.0254, 0.071, 0.08, 0.0198, 0.0012, 0.0683, 
             0.061,  0.1047, 0.0246, 0.0092, 0.0154, 0.0017, 0.0198, 0.0008]
ic_english_letters = {letter: ic for letter, ic in zip(alphabet, en_ics_lst)}
shift_dict = {letter: alphabet.index(letter) for letter in alphabet}

fi = open('input1.txt', 'r', encoding='utf8')
rawtxt = ''.join(line for line in fi)
cleantxt = ''.join([c for c in rawtxt if c.isalpha()])

ic_lst, all_periods_ics = [], []
for i in range(1, len(cleantxt)):
    period_sub_ics = []
    if i > 50:
        break
    for y in range(i):
        sequence, ic_lst = cleantxt[y::i], []
        if len(sequence) == 1:
            break
        ic_lst = [sequence.count(l) * (sequence.count(l) - 1) for l in alphabet]
        ic_avg = sum(ic_lst) / (len(sequence) * (len(sequence) - 1))
        period_sub_ics.append(ic_avg)
    period_ic = sum(period_sub_ics) / len(period_sub_ics)
    all_periods_ics.append(period_ic)
    print(i, period_ic)
if len(all_periods_ics) > 1:
    overall_avg_period_ic = sum(all_periods_ics) / len(all_periods_ics)
    keylen_candidates = [(keylen, ic) for keylen, ic in enumerate(all_periods_ics, start=1)
                                                             if ic > overall_avg_period_ic]
    keylen = min(k[0] for k in keylen_candidates)
print(keylen)

s, key_cipher = 0, ''
while s < keylen:
    sequence = cleantxt[s::keylen]
    avg_chi_lst = []
    for i in range(len(alphabet)):
        new_sequence = []
        for letter in sequence:
            letter = (chr(ord(letter)-i) if i<=shift_dict[letter] else chr(ord(letter)+(26-i)))
            new_sequence.append(letter)
        new_sequence = ''.join(new_sequence)
        
        chi_lst = []
        for letter in new_sequence:
            expected_count = ic_english_letters[letter] * len(new_sequence)
            chi_sq = ((new_sequence.count(letter) - expected_count) ** 2) / expected_count
            chi_lst.append(chi_sq)

        avg_chi = sum(chi_lst) / len(chi_lst)
        avg_chi_lst.append(avg_chi)
        print(i, new_sequence, avg_chi)
    key_letter = alphabet[avg_chi_lst.index(min(avg_chi_lst))]
    key_cipher += key_letter
    s += 1
print(key_cipher)

newstr, i = [], 0
for char in rawtxt:
    if char.isalpha():
        new_ord, shift = ord(char) - shift_dict[key_cipher[i]], shift_dict[key_cipher[i]]
        char = (chr(new_ord) if new_ord >= ord('a') else chr(ord(char) + (26 - shift)))
        i =  i + 1 if i < (len(key_cipher) - 1) else 0
    newstr.append(char)
newstr = ''.join(newstr)

txt_ic_lst = [newstr.count(c)/len(cleantxt) for c in newstr if c.isalpha()]
txt_ic = sum(txt_ic_lst) / len(txt_ic_lst)

print(newstr)
print('\ntext ic = {}'.format(txt_ic))
