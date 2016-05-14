var fl = document.getElementById('attachedFiles');

fl.onchange = function(e){ 
    var ext = this.value.match(/\.([^.]+)$/)[1];
        switch(ext)
        {
             case 'jpg':
             case 'csv':
             case 'doc':
             case 'docx':
             case 'jpeg':
             case 'pdf':
             case 'ppt':
             case 'rtf':
             case 'txt':
             case 'bmp':
             case 'png':
             case 'tif':
             case 'tar':
             case 'zip':
                 break;
             default:
                 alert('File type not allowed');
                 this.value='';  
         }
};
