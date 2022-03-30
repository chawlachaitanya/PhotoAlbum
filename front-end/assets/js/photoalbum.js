let recognition;
$(window).load(function (){
    window.SpeechRecognition = window.SpeechRecognition
                        || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
        
})

function recognize(){
    try{
        recognition.onresult = function(event) {

            // event is a SpeechRecognitionEvent object.
            // It holds all the lines we have captured so far. 
            // We only need the current one.
            var current = event.resultIndex;
            
            // Get a transcript of what was said.
            var transcript = event.results[current][0].transcript;
            document.getElementById('searchQueryText').value=transcript;
            searchResults()
            // Add the current transcript to the contents of our Note.
            console.log(transcript)
    
        }
        recognition.start()
    } catch (exception){
        alert('Not supported')
    }
    

}

function uploadFile(){
    let labelsList=document.getElementById("customLabels").value.replace(/\s+/g, '')
    console.log(labelsList)
    const fileName=document.getElementById("imageFile").value.replace(/^.*\\/, "");
    const fileElement=document.getElementById("imageFile")
    if ((!'files' in fileElement) || fileElement['files'].length<=0){
        return;
    }
    img=document.getElementById("imageFile").files[0];
    console.log(img)
    url='https://e6qjv5bg4l.execute-api.us-east-1.amazonaws.com/v1/upload/'+fileName
    fetch(url,{
        method:'PUT',
        body:img,
        headers: {
          "X-Api-Key": 'chawlachawlachawlachawlachawla',
          "Content-Type": "image/png",
          'x-amz-meta-customLabels': labelsList
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