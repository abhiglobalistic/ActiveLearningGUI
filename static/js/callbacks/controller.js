
function getSamples_toAnnotate() {

  counts = localStorage.getItem('stepSampleCount')
  var count_data = {}
  count_data['stepSampleCount'] = counts


  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

        getSamplesBtn = document.getElementById('getButton')
        toggleButton(getSamplesBtn)

        submitLabelsBtn = document.getElementById('subButton')
        toggleButton(submitLabelsBtn)

        setCurrentCount();
        var c = parseInt(0)
        samplesData = JSON.parse(this.responseText)

        samplesData.forEach(function(samples){

            samples.forEach(function(sample){


                var tr = document.createElement('TR')
                var td = document.createElement('TD')
                var audio = document.createElement('AUDIO')
                audio.title = sample.name
                audio.src = sample.clip
                audio.controls = 'controls'
                audio.load();
                td.appendChild(audio)
                tr.appendChild(td)
                tr.appendChild(getSelDropdown())

                if(c < 5){
                    logReg_table = document.getElementById('logReg_table')
                    logReg_table.appendChild(tr)
                }

                 if(c >= 5 && c < 10){
                    svm_table = document.getElementById('svm_table')
                    svm_table.appendChild(tr)
                }


                 if(c >= 10 && c < 15){
                    rfc_table = document.getElementById('rfc_table')
                    rfc_table.appendChild(tr)
                }

                c += 1;


            })

        });

    }
  };
  xhttp.open("POST", "http://127.0.0.1:5000/getsamples", false);
  xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhttp.send(JSON.stringify(count_data));
}

function send_AnnotatedSamples()
{
     var logReg_table = document.getElementById("logReg_table")
     var svm_table = document.getElementById("svm_table")
     var rfc_table = document.getElementById("rfc_table")

      var tablesData = [logReg_table,svm_table,rfc_table]

        data = []
        tablesData.forEach(function(tableData){

            j = 0
            while(j < tableData.rows.length){
                cell = tableData.rows[j]
                audio_name = cell.children[0].children[0].title;
                selectedLabel = cell.children[1].children[0]
                selectedLabel = selectedLabel.options[selectedLabel.selectedIndex].text
                samp = {}
                samp[audio_name] = selectedLabel
                data.push(samp)
                j++;

            }

         });

     var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {

            console.log(this.responseText)
            scores = JSON.parse(this.responseText)

            for (score in scores){
                document.getElementById(score).innerHTML = scores[score]+'%';
            }

            tablesData.forEach(function(tableData){
                while(tableData.hasChildNodes()){
                    tableData.removeChild(tableData.firstChild)
                }
             });

            submitLabelsBtn = document.getElementById('subButton')
            toggleButton(submitLabelsBtn)

            getSamplesBtn = document.getElementById('getButton')
            toggleButton(getSamplesBtn)

            generateGraph()
        }
      };
      xhttp.open("POST", "http://127.0.0.1:5000/train", false);
      xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
      xhttp.send(JSON.stringify(data));
}


function setCurrentCount(){
    var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {

            localStorage.setItem('stepSampleCount',this.responseText)
        }
      };
      xhttp.open("GET", "http://127.0.0.1:5000/currentCount", true);
      xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
      xhttp.send();
}


function onBoot() {

    submitLabelsBtn = document.getElementById('subButton')
    toggleButton(submitLabelsBtn)

    boot()
    generateGraph()
}


function boot(){
    var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
              data = JSON.parse(this.responseText)

              for(item in data){
                    var td = document.createElement('TH')
                    var btn = document.createElement('BUTTON')
                    btn.innerHTML = item +'  <span id='+item+' class="badge badge-light">'+data[item]+'% </span>'
                    btn.classList.add('btn')
                    btn.classList.add('btn-primary');
                    td.appendChild(btn)
                    document.getElementById('stats').appendChild(td)
              }



        }
      };
      xhttp.open("GET", "http://127.0.0.1:5000/onboot", true);
      xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
      xhttp.send();
}


function generateGraph() {
    var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
              data = JSON.parse(this.responseText)
                var graphs = data
                Plotly.newPlot('chart',graphs,{})
        }
      };
      xhttp.open("GET", "http://127.0.0.1:5000/graph",false);
      xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
      xhttp.send();
}


function getSelDropdown(){


          var tdsel = document.createElement('TD')
          var select = document.createElement('SELECT')
          select.classList.add('form-control')
          select.selected = 'female'
          var optMale = document.createElement('OPTION')
          optMale.value = 'male'
          optMale.text = 'male'
          var optFml = document.createElement('OPTION')
          optFml.value = 'female'
          optFml.text = 'female'
          select.appendChild(optMale)
          select.appendChild(optFml)
          tdsel.appendChild(select)


    return tdsel
}

function toggleButton(btn){
    if(btn.disabled == false){
        btn.disabled = true
    }else {
        btn.disabled = false
    }
   }