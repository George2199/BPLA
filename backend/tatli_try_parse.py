import json

with open("/home/nout/vue/BPLA_main/backend/data/blocks_1.json", "r", encoding="utf-8") as f:
    parse_data = json.load(f)

    # print(parse_data)

    # for b in parse_data["blocks"]:
    #     a = b['cat']
    #     c = b['type']
    #     print(a)
    #     print(c)

    types = set([i['type'] for i in parse_data["blocks"]])
    print(types)