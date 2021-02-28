# import os
def configInp(inp_file_path,out_file_path,options=[],values=[]):
  '''
  description: modify the options of an inpfile
  :param inp_file_path: <string> absolute path of inp file
  :param out_file_path: <string> absolute path of output file, default identical to inp_file_path
  :options: <[string]> option(s) to be modified
  :values: <[string]> value(s) to be assigned, if not specified, the original value will be add into ret
  return :: dict{
              'option1': 'value1',
              'option2': 'value2',
              ...
            }
  '''
  # if the out_file_path is not specified, use inp_file_path instead
  if not out_file_path or out_file_path == '':
    out_file_path = inp_file_path
  # the ret dict
  ret = {}
  optionsNum = len(options)
  # read the inp file
  with open(inp_file_path,'r')as inp :
    lines = inp.readlines()
    cnt = 0
    for i,v in enumerate(lines):
      # if the option matches one of the option in options
      if len(v.split())>0 and v.split()[0] in options:
        # check if there is a new value (nv)
        if values and values.length and values[options.index(v.split()[0])] != '':
          nv = values[options.index(v.split()[0])]
          # modify option
          lines[i] = str(v.split()[0]) + '            '+values[options.index(v.split()[0])]+'\n'
        # else set the original to nv
        else:
          nv = v.split()[1] 
        # add the value to ret dict
        ret[v.split()[0]] = nv
        cnt += 1
      # if the options are all set, stop the iteration
      if(cnt == optionsNum):
        break
  # write the inp file (replace the original file)
  if values and values.length > 0:
    with open(out_file_path,'w') as output:
      output.writelines(lines)
  # NOTE: NOT CHECKED
  return ret
# publicPath = os.path.abspath(os.path.join(os.getcwd()))
# inp_file_path = os.path.join(publicPath,'mock','random','try-case.inp')
# configInp(inp_file_path,inp_file_path,['FLOW_UNITS','MIN_SLOPE'],['LSP','100'])