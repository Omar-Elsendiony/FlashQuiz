
var selectedItem = null;
const questions = new Array(0);
const questions_options = new Array(0);
const correct_choice = new Array(0);
var quiz_title;
var quiz_description;
var question_index = 0
var questions_total = 1
var cross = [true,true,true,true] // it is cross by default
var selected_correct = -1
node_selected = null


var enumerate = {"one": 1, "two": 2, "three": 3, "four": 4};

function optionSelected(element) {
    index = enumerate[element.parentNode.id] - 1
    cross[index] = !cross[index];
    if (!cross[index]){
        if (node_selected != null) {
            // correct = options[i].value;
            node_selected.style.backgroundColor = "#FF7F7F";
            node_selected.style.borderColor = "red";
            node_selected.innerHTML = "&#x274c"
            cross[enumerate[node_selected.parentNode.id] - 1] = true
        }

        element.style.backgroundColor = "green";
        element.style.borderColor = "green";
        element.innerHTML = "&#x2705"
        node_selected = element
        selected_correct = enumerate[element.parentNode.id]
    }
    else{
        node_selected = null
        element.style.backgroundColor = "#FF7F7F";
        element.style.borderColor = "red";
        element.innerHTML = "&#x274c"
    }
}



setTimeout(() => {

document.getElementById('startButton').addEventListener('click',
    function(event) {
        document.querySelector('.rules_data').style.display = "none";
        document.querySelector('.meta_data').style.display = "block";
});

document.getElementById('startQuestion').addEventListener('click',
    function(event) {
        quiz_title = document.getElementById('quiz_meta_title').value
        quiz_description = document.getElementById('quiz_meta_description').value
        if (quiz_title == "" || quiz_description == ""){
            alert("Please fill all the fields")
            return
        }
        document.getElementById('test_title').innerHTML = quiz_title

        document.querySelector('.meta_data').style.display = "none";
        document.querySelector('.question_creation').style.display = "block";
        // updateQuestion("add")
        document.getElementById('numberQuestion').innerHTML = "Question " + (question_index + 1) + " of " + (questions_options.length + 1);

});

function updateQuestion(status) {
    if (status == "add") {
        question_index += 1;
        if (question_index == questions_options.length) {
            document.getElementById('numberQuestion').innerHTML = "Question " + (question_index + 1) + " of " + (questions_options.length);
        }else{
            document.getElementById('numberQuestion').innerHTML = "Question " + (question_index + 1) + " of " + (questions_options.length);        
        }
    } else {
        question_index -= 1;
        document.getElementById('numberQuestion').innerHTML = "Question " + (question_index + 1) + " of " + (questions_options.length);
    }

}


document.getElementById('add').addEventListener('click',
    function(event) {

        var question = document.querySelector('.que_text').value;
        console.log(question)
        if (question == ""){
            alert("Please fill the question")
            return;
        }

        // var correct = null;
        // var options = document.querySelectorAll('.option');
        // for (let i = 0; i < options.length; i++) {
        //     if (options[i].parentNode.style.backgroundColor == "lightgreen") {
        //         correct = options[i].value;
        //     }
        // }
        if (node_selected == null){
            alert("Please select the correct answer")
            return;
        }
        correct = node_selected.nextElementSibling.value
        console.log(node_selected.nextElementSibling)
        inputs = document.querySelectorAll('.option input')


        for (let i = 0; i < inputs.length; i++) {
            console.log(inputs[i].value)
            if (inputs[i].value == "") {
                alert("Please fill all the options")
                return;
            }
        }

        let inputs_values = new Array();
        for (let i = 0; i < inputs.length; i++) {
            inputs_values.push(inputs[i].value)
        }

        questions[question_index] = question
        questions_options [question_index] = (inputs_values)
        correct_choice[question_index] = (correct)

        questions.push(question)
        questions_options.push(inputs_values)
        correct_choice.push(correct)

        // console.log(questions_options)
        // console.log(questions)

        updateQuestion("add")

        /// reset the input fields ///
        document.querySelector('.que_text').value = ""
        for (let i = 0; i < inputs.length; i++) {
            inputs[i].value = ""
        }

        selected_correct = -1
        node_selected = null

        labels = document.getElementsByClassName('labelFormat')
        for (let i = 0; i < labels.length; i++) {
            labels[i].innerHTML =  "&#x274c"
            labels[i].style.backgroundColor = "#FF7F7F";
        }

        
        for (let i = 0; i < cross.length; i++) {
            cross[i] = true
        }
});


document.getElementById('next').addEventListener('click',
    function(event) {
        var question = document.querySelector('.que_text').value;
        if (question == ""){
            alert("Please fill the question")
            return;
        }

        for (let i = 0; i < inputs.length; i++) {
            if (inputs[i].value == "") {
                alert("Please fill all the options")
                return;
            }
        }

        if (node_selected == null){
            alert("Please select the correct answer")
            return;
        }
        
        correct = node_selected.nextElementSibling.value
        correct_choice[question_index] = correct

        let inputs_values = new Array();
        for (let i = 0; i < inputs.length; i++) {
            inputs_values.push(inputs[i].value)
        }
        questions_options[question_index] = inputs_values

        // the next question
        updateQuestion("add")

        if (question_index == questions_options.length - 1) {
            document.getElementById('add').style.display = "block";
            document.getElementById('next').style.display = "none";
        }

        document.querySelector('.que_text').value = questions[question_index]

        // populating the labels with cross
        labels = document.getElementsByClassName('labelFormat')
        for (let i = 0; i < labels.length; i++) {
            labels[i].innerHTML =  "&#x274c"
            labels[i].style.backgroundColor = "#FF7F7F";
        }

        inputs = document.querySelectorAll('.option input')
        for (let i = 0; i < inputs.length; i++) {
            inputs[i].value = questions_options[question_index][i]
            if (inputs[i].value == correct_choice[question_index]) {
                inputs[i].previousElementSibling.innerHTML = "&#x2705"
                inputs[i].previousElementSibling.style.backgroundColor = "green";
                inputs[i].previousElementSibling.style.borderColor = "green";
                node_selected = inputs[i].previousElementSibling
            }
        }

        // node_selected = null
        // selected_correct = -1

        for (let i = 0; i < cross.length; i++) {
            cross[i] = true
        }
        
        console.log(correct_choice)
});




document.getElementById('previousButton').addEventListener('click',
    function(event) {
        if (question_index == 0) {
            document.querySelector('.meta_data').style.display = "block";
            document.querySelector('.question_creation').style.display = "none";
            return
        }

        var question = document.querySelector('.que_text').value;
        if (question == ""){
            alert("Please fill the question")
            return;
        }

        for (let i = 0; i < inputs.length; i++) {
            // console.log(inputs[i].value)
            if (inputs[i].value == "") {
                alert("Please fill all the options")
                return;
            }
        }

        questions[question_index] = document.querySelector('.que_text').value
        inputs = document.querySelectorAll('.option input')
        inputs_values = new Array();

        for (let i = 0; i < inputs.length; i++) {
            inputs_values.push(inputs[i].value)
        }

        questions_options[question_index] = inputs_values


        if (node_selected == null){
            alert("Please select the correct answer")
            return;
        }

        correct = node_selected.nextElementSibling.value
        correct_choice[question_index] = correct


        /////////// start changing to the virtual previous page /////////////
        document.getElementById('add').style.display = "none";
        document.getElementById('next').style.display = "block";

        updateQuestion("sub")

        document.querySelector('.que_text').value = questions[question_index]
        inputs = document.querySelectorAll('.option input')

        // populating the labels with cross
        labels = document.getElementsByClassName('labelFormat')
        for (let i = 0; i < labels.length; i++) {
            labels[i].innerHTML =  "&#x274c"
            labels[i].style.backgroundColor = "#FF7F7F";
        }


        for (let i = 0; i < inputs.length; i++) {
            inputs[i].value = questions_options[question_index][i]
            if (inputs[i].value == correct_choice[question_index]) {
                inputs[i].previousElementSibling.innerHTML = "&#x2705"
                inputs[i].previousElementSibling.style.backgroundColor = "green";
                inputs[i].previousElementSibling.style.borderColor = "green";
                node_selected = inputs[i].previousElementSibling
            }
        }

});


function submitContent() {
    let headers = new Headers();
    headers.append('Content-Type', 'application/json');
    // headers.append('Access-Control-Allow-Origin', 'http://127.0.0.1:5000');
    headers.append('Access-Control-Allow-Credentials', 'true');

    fetch("/test_create", {
            method: "POST",
            body: JSON.stringify({
                "quiz_title": quiz_title,
                "quiz_description": quiz_description,
                "questions": questions,
                "questions_options": questions_options,
                "correct_choice": correct_choice
            }),
            headers: headers
        })
        .then((response) => response.json())
        .then((json) => console.log(json));
}



document.getElementById('submit').addEventListener('click',
    function(event) {

        var question = document.querySelector('.que_text').value;
        if (question == ""){
            alert("Please fill the question")
            return;
        }
        
        var inputs = document.querySelectorAll('.option input')
        for (let i = 0; i < inputs.length; i++) {
            if (inputs[i].value == "") {
                alert("Please fill all the options")
                return;
            }
        }
        questions[question_index] = document.querySelector('.que_text').value
        inputs = document.querySelectorAll('.option input')
        inputs_values = new Array();
        
        for (let i = 0; i < inputs.length; i++) {
            inputs_values.push(inputs[i].value)
        }


        questions_options[question_index] = inputs_values

        if (node_selected == null){
            alert("Please select the correct answer")
            return;
        }

        correct = node_selected.nextElementSibling.value
        correct_choice[question_index] = correct

        /////////// start submitting the content of the question, options and title /////////////
        submitContent()
        document.querySelector('.question_creation').style.display = "none";
        document.querySelector('.success_column').style.display = "block";
});

}, 1000);






/////////////////////////////////////////////////////
//////////////// ANIMATE RUBIK //////////////////////
////////////////////////////////////////////////////

setTimeout(() => {
    var start = true
    var direction = "down";
    function downToUp() {
        $("#floatingRubik").animate({ top: '-=50%' }, 10000, function() {
                animateElement(); 
        })};


    function upToDown() {
        $("#floatingRubik").animate({ top: '+=50%' }, 10000, function() {
                animateElement();
        })};

    function animateElement() {
        var parentElement = document.getElementsByClassName('playing_rubik')[0];
        visibilityParent = parentElement.checkVisibility();
        // console.log(visibilityParent)
        if (visibilityParent == false){
            return
        }

        var element = document.getElementById('floatingRubik');

        // console.log(screen.height)
        
        var position = element.getBoundingClientRect();
        var x = position.left;
        var y = position.top;
        // console.log(y)
        
        if (start == true) {
            start = false;
            upToDown();
        }
        else{
            // console.log("else")
            if (y > 0.3 * screen.height ) {
                direction = "up";
                // rightToLeft();
            }
            if (y <= 0.3 * screen.height) {
                direction = "down"
                // leftToRight();
            }
            if (direction == "down") {
                upToDown();
            }
            else{
                downToUp();
            }
        }
    }
    // Start the animation
    animateElement();

}, 50);
