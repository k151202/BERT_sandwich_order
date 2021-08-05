import src.data_generate_yehoon as yh
import src.data_generate_jungmin as jm
import src.data_generate_jongrin as jr
import src.data_generate_taehyung as th
import src.data_generate_jihun as jh
import src.data_generate_changhun as ch


data = []

data.extend(yh.gen_data())
data.extend(jm.gen_data())
data.extend(jr.gen_data())
data.extend(th.gen_data())
data.extend(jh.gen_data())
data.extend(ch.gen_data())

data = set(data)

with open("data.txt", "w", encoding="utf-8") as f:
  for sentence in data:
    f.write(sentence+"\n")
