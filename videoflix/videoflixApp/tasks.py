import subprocess

def convert_480p(source):    
    new_file_name = source+"_480.mp4" 
    print(source)
    cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file_name)  # {} wird durch dass was bei source bzw. target angegeben ist ersetzt  
    #run = subprocess.run(cmd, capture_output=True)
    run = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    
def convert_720p(source):    
    new_file_name = source+"_720.mp4" 
    print(source)
    cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file_name)    
    #run = subprocess.run(cmd, capture_output=True)
    run = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
def convert_1080p(source):    
    new_file_name = source+"_1080.mp4" 
    print(source)
    cmd = 'ffmpeg -i "{}" -s hd1080 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file_name)    
    #run = subprocess.run(cmd, capture_output=True)
    run = subprocess.run(cmd, shell=True, capture_output=True, text=True)