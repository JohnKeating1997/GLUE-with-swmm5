# import os
def configInp(inp_file_path,out_file_path,options=[],values=[]):
  '''
  description: modify the options of an inpfile
  :param inp_file_path: <string> absolute path of inp file
  :param out_file_path: <string> absolute path of output file, default identical to inp_file_path
  :options: <[string]> option(s) to be modified
  :values: <[string]> value(s) to be assigned
  return {*}
  '''
  optionsNum = len(options)
  with open(inp_file_path,'r')as inp :
    lines = inp.readlines()
    cnt = 0
    for i,v in enumerate(lines):
      if len(v.split())>0 and v.split()[0] in options:
        # 修改option
        lines[i] = str(v.split()[0]) + '            '+values[options.index(v.split()[0])]+'\n'
        cnt += 1
      if(cnt == optionsNum):
        break
  with open(out_file_path,'w') as output:
    output.writelines(lines)

# publicPath = os.path.abspath(os.path.join(os.getcwd()))
# inp_file_path = os.path.join(publicPath,'mock','random','try-case.inp')
# configInp(inp_file_path,inp_file_path,['FLOW_UNITS','MIN_SLOPE'],['LSP','100'])