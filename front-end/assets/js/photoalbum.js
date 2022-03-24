function upload(image, labels){

}
function uploadFile(){
    const fileName=document.getElementById("imageFile").value.replace(/^.*\\/, "");
    img=document.getElementById("imageFile").files[0];
    console.log(img)
    url='https://e6qjv5bg4l.execute-api.us-east-1.amazonaws.com/v1/upload/'+fileName
    fetch(url,{
        method:'PUT',
        body:img,
        headers: {
          "X-Api-Key": 'chawlachawlachawlachawlachawla',
          "Content-Type": "image/png"
      }
    }).then(response => console.log(response))
  .catch(error => console.log('Error while fetching:', error));

    // sdk.uploadItemPut({'item':fileName, 'Content-Type': 'img/jpg'},img, {})
    // .then((response)=>console.log(response))
    // .catch((error)=>console.log(error));
}

function searchResults(){
    const searchResults=document.getElementById('searchResults');
    console.log(searchResults)
    searchResults.removeChild(searchResults.firstChild)

    var results = document.createElement('div');
    results.className='searchResults';

    
    searchResults.appendChild(results);

    const searchQuery=document.getElementById('searchQueryText').value;
    sdk.searchGet({'q': searchQuery}, {}, {})
    .then((response)=>{
        data=response.data;
        console.log(data)
        for(let i=0;i<data.length;i++){
            var fig=document.createElement('figure');
            var img = document.createElement('img');
            var figcaption=document.createElement('figcaption');
            img.src = data[i].url;
            img.height=300;
            img.width=300;
            img.alt='Image has been removed from s3 but not open search'
            figcaption.innerHTML=data[i].labels;
            fig.appendChild(img);
            fig.appendChild(figcaption);
            
            results.appendChild(fig)

        }
    })
    .catch((error)=>{
        console.log(error)
    })
}