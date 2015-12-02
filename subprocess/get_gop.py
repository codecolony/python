import subprocess

# subprocess.call(["ls", "-l", "-a"])

outp = subprocess.check_output(["matlab", "-nodisplay", "-nosplash", "-nodesktop", "-r", "run('/path/to/GOP/matlab/test.m');exit;"])

idx_hash = outp.index("#")
outp = outp[idx_hash+1:]

#print "Output goes here"
print outp

# C:\<a long path here>\matlab.exe" -nodisplay -nosplash -nodesktop -r "run('C:\<a long path here>\mfile.m');exit;"