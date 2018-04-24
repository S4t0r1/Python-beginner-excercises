def attack(inFile, outFile):
  fi = open(inFile, 'r', encoding='utf8')
  newtxt = []
  for line in fi:
      newline = ''.join(char for char in line.strip() if char.isalpha())
      newtxt.append(newline)
  newtxt = ''.join(newtxt)
  print(newtxt)
  
  alphabet = "abcdefghijklmnopqrstuvwxyz"
  ic = None
  ic_lst = []
  n = len(newtxt)
  for letter in alphabet:
      ic_letter = newtxt.count(letter) * (newtxt.count(letter) - 1)
      ic_lst.append(ic_letter)
  
  avg_ic = sum(ic_lst) / (len(newtxt) * (len(newtxt) - 1))
  print()
  print(avg_ic)
  
  ic_lst = []
  period_avg = []
  for i in range(1, len(newtxt)):
      for y in range(i):
          sequence = newtxt[y::i]
          if len(sequence) == 1:
              break
          for letter in alphabet:
              ic = sequence.count(letter) * (sequence.count(letter) - 1)
              ic_lst.append(ic)
          ic_avg = sum(ic_lst) / (len(sequence) * (len(sequence) - 1))
          period_avg.append(ic_avg)
          ic_lst = []
      period_ic = sum(period_avg) / len(period_avg)
      period_avg = []
      print(i, period_ic)
  
  ic_english_letters = {}
  ics_lst = [0.0815, 0.0144, 0.0276, 0.0379, 0.1311, 0.0292, 0.0199, 0.0526, 0.0635, 
             0.0013, 0.0042, 0.0339, 0.0254, 0.071, 0.08, 0.0198, 0.0012, 0.0683, 
             0.061,  0.1047, 0.0246, 0.0092, 0.0154, 0.0017, 0.0198, 0.0008]
  for letter, ic in zip(alphabet, ics_lst):
      ic_english_letters[letter] = ic
  
  for e in range(i):
      our_sequence = newtxt[e::7]
      for letter in alphabet:
          chi_sq = (our_sequence.count(letter) - ic_english_letters[letter]) ** 2 / ic_english_letters[letter]
          

attack("test2.txt", "out1.txt")
