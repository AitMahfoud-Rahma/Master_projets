import pandas as pd

cusp_file = r'/home/aitmahfoud/Documents/GECO/TP2/emboss/pylori/cusp_pylori.cusp'

# 使用read_csv来读取Cusp文件，使用逗号作为分隔符
df = pd.read_csv(cusp_file, sep=',', header=None)

# 指定输出文件的完整路径
excel_file = r'D:\0-AMU\DLAD\6-GecO\PROJET-TP1\cusp_files\2.2_cusp_cds.xlsx'

# 将数据保存为Excel文件
df.to_excel(excel_file, index=False, header=False)

