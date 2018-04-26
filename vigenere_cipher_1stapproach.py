

def attack(inFile, outFile):
  fi = open(inFile, 'r', encoding='utf8')
  newtxt = []
  for line in fi:
      newline = ''.join(char for char in line.strip() if char.isalpha())
      newtxt.append(newline)
  newtxt = ''.join(newtxt)
  print(newtxt)
  print(len(newtxt))
  
  alphabet = "abcdefghijklmnopqrstuvwxyz"
  alphabet_dict = {alphabet.index(letter): letter for letter in alphabet}
  
  ic_lst = []
  all_periods_ics = []
  for i in range(1, len(newtxt)):
      period_sub_ics = []
      if i > 50:
          break
      for y in range(i):
          sequence = newtxt[y::i]
          if len(sequence) == 1:
              break
          for letter in alphabet:
              ic = sequence.count(letter) * (sequence.count(letter) - 1)
              ic_lst.append(ic)
          ic_avg = sum(ic_lst) / (len(sequence) * (len(sequence) - 1))
          period_sub_ics.append(ic_avg)
          ic_lst = []
      period_ic = sum(period_sub_ics) / len(period_sub_ics)
      all_periods_ics.append(period_ic)
      print(i, period_ic)
  if len(all_periods_ics) > 1:
      overall_avg_period_ic = sum(all_periods_ics) / len(all_periods_ics)
      keylen_candidates = [(keylen, ic) for keylen, ic in enumerate(all_periods_ics, start=1)
                                                         if ic > overall_avg_period_ic]
      keylen = min(k[0] for k in keylen_candidates)
  print(keylen)
  
  
  ics_lst = [0.0815, 0.0144, 0.0276, 0.0379, 0.1311, 0.0292, 0.0199, 0.0526, 0.0635, 
             0.0013, 0.0042, 0.0339, 0.0254, 0.071, 0.08, 0.0198, 0.0012, 0.0683, 
             0.061,  0.1047, 0.0246, 0.0092, 0.0154, 0.0017, 0.0198, 0.0008]
  ic_english_letters = {letter: ic for letter, ic in zip(alphabet, ics_lst)}
  
  s, key_cipher = 0, ''
  while s < keylen:
      our_sequence = newtxt[s::keylen]
      avg_chi_lst = []
      for i in range(len(alphabet)):
          next_sequence = []
          for letter in our_sequence:
              for key in alphabet_dict.keys():
                  if alphabet_dict[key] == letter:
                      keynum = 26 + (key - i) if (key - i) < 0 else key - i
                      letter = alphabet_dict[keynum]
                      next_sequence.append(letter)
                      break
          next_sequence = ''.join(next_sequence)
          chi_lst = []
          for letter in next_sequence:
              expected_count = ic_english_letters[letter] * len(next_sequence)
              chi_sq = ((next_sequence.count(letter) - expected_count) ** 2) / expected_count
              chi_lst.append(chi_sq)
          avg_chi = sum(chi_lst) / len(chi_lst)
          avg_chi_lst.append(avg_chi)
          print(i, next_sequence, avg_chi)
      key_letter = alphabet_dict[avg_chi_lst.index(min(avg_chi_lst))]
      key_cipher += key_letter
      s += 1
  print(key_cipher)
  
  rev_alpha_dict = {v: k  for k, v in alphabet_dict.items()}
  fh = open(inFile, 'r', encoding='utf8')
  rawtxt = ''.join(line for line in fh)
  newstr, i = '', 0
  for char in rawtxt:
      if char.isalpha():
          charv, letterv = rev_alpha_dict[char], rev_alpha_dict[key_cipher[i]]
          new_charv = 26 + (charv - letterv) if (charv - letterv) < 0 else charv - letterv
          char = alphabet_dict[new_charv]
          i =  i + 1 if i < (len(key_cipher) - 1) else 0
      newstr += char
  print(newstr)
  
  
attack("input1.txt", "out1.txt")
