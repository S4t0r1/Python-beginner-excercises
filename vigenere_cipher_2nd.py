

alphabet = "abcdefghijklmnopqrstuvwxyz"
shift_dict = {letter: alphabet.index(letter) for letter in alphabet}

en_ics_lst = [0.0815, 0.0144, 0.0276, 0.0379, 0.1311, 0.0292, 0.0199, 0.0526, 0.0635, 
              0.0013, 0.0042, 0.0339, 0.0254, 0.071, 0.08, 0.0198, 0.0012, 0.0683, 
              0.061,  0.1047, 0.0246, 0.0092, 0.0154, 0.0017, 0.0198, 0.0008]
en_ics = {letter: ic for letter, ic in zip(alphabet, en_ics_lst)}

rawtxt = ''.join(line for line in open('input1.txt', 'r', encoding='utf8'))
cleantxt = ''.join([c for c in rawtxt if c.isalpha()])

all_periods_ics = []
for i in range(1, 20):
    period_sub_ics = []
    for y in range(i):
        sequence, ic_lst = cleantxt[y::i], []
        if len(sequence) < 2:
            break
        ic_lst = [sequence.count(l) * (sequence.count(l) - 1) for l in alphabet]
        period_sub_ics.append(sum(ic_lst) / (len(sequence) * (len(sequence) - 1)))
    all_periods_ics.append(sum(period_sub_ics) / len(period_sub_ics))

keylen_candidates = [(keylen, ic) for keylen, ic in enumerate(all_periods_ics, start=1)
                                   if ic > sum(all_periods_ics) / len(all_periods_ics)]
keylen = min(k[0] for k in keylen_candidates)

s, key_cipher = 0, []
while s < keylen:
    init_str, avg_chi_lst = cleantxt[s::keylen], []
    for i in range(len(alphabet)):
        new_str = ''.join([(chr(ord(let) - i) if i <= shift_dict[let] 
                       else chr(ord(let) + (26 - i))) for let in init_str])
        exp_count = {l: en_ics[l] * len(new_str) for l in new_str}
        chi_lst = [((new_str.count(l) - exp_count[l]) ** 2) / exp_count[l] for l in new_str]
        avg_chi_lst.append(sum(chi_lst) / len(chi_lst))
    key_cipher.append(alphabet[avg_chi_lst.index(min(avg_chi_lst))])
    s += 1
key_cipher = ''.join(key_cipher)

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

print(newstr, '\ntext ic = {}'.format(txt_ic))
