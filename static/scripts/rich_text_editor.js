#!/usr/bin/node
setTimeout(() => {
    const elements = document.querySelectorAll('.btn');

    content_element = document.querySelectorAll('.content')[0];
    // console.log(content_element);

    // $(document).on('keyup', function(){
    //     content_element.setAttribute("contenteditable","false")
    //     var $newChild=$('hello'); 
    //     $('.content').append($newChild);
    // });

    // elements.forEach(element => {
    //     element.addEventListener('click', () => {
    //         let command = 'em';
    //         content_element.innerHTML += '<' + command + '></' + command + '>';
    //         content_element.innerHTML += 'added';
    //     });
    // });
}, 50);

