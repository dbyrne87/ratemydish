$(function () {
    $('#btnAdd_1').click(function () {
        var num     = $('.clonedInput_1').length, // Checks to see how many "duplicatable" input fields we currently have
            newNum  = new Number(num + 1),      // The numeric ID of the new input field being added, increasing by 1 each time
            newElem = $('#entry' + num).clone().attr('id', 'entry' + newNum).fadeIn('slow'); // create the new element via clone(), and manipulate it's ID using newNum value

        // Label for input_ingredients field
        newElem.find('.ingredients_label').attr('id', 'Field' + newNum + '_reference').attr('name', 'Field' + newNum + '_reference').html('Step #' + newNum);

        // input_ingredients input - text
        newElem.find('.label_ingredients').attr('id', 'Field' + newNum + '_input_ingredients').attr('name', 'Field' + newNum + '_input_ingredients').val=("");

    // Insert the new element after the last "duplicatable" input field
        $('#entry' + num).after(newElem);
        $('input[id=Field' + newNum +'_input_ingredients]').val('');
        $('#Field' + newNum + '_title').focus();
        

    // Enables the "remove" button. This only shows once you have a duplicated section.
        $('#btnDel_1').attr('disabled', false);

        // How many Fields are allowed
        if (newNum == 10)
        $('#btnAdd_1').attr('disabled', true).prop('value', "You've reached the limit"); // value here updates the text in the 'add' button when the limit is reached
    });

    $('#btnDel_1').click(function () {
    // Confirmation dialog box. Works on all desktop browsers and iPhone.
        if (confirm("Are you sure you wish to remove this field? This cannot be undone."))
            {
                var num = $('.clonedInput_1').length;
                // how many "duplicatable" input fields we currently have
                $('#entry' + num).slideUp('slow', function () {$(this).remove();
                // if only one element remains, disable the "remove" button
                    if (num -1 === 1)
                $('#btnDel_1').attr('disabled', true);});
            }
        return false; // Removes the last section you added
    });
    // Enable the "add" button
    $('#btnAdd_1').attr('disabled', false);
    // Disable the "remove" button
    $('#btnDel_1').attr('disabled', true);





    $('#btnAdd_2').click(function () {
        var num     = $('.clonedInput_2').length, // Checks to see how many "duplicatable" input fields we currently have
            newNum  = new Number(num + 1),      // The numeric ID of the new input field being added, increasing by 1 each time
            newElem = $('#phone' + num).clone().attr('id', 'phone' + newNum).fadeIn('slow'); // create the new element via clone(), and manipulate it's ID using newNum value
    
    /*  This is where we manipulate the name/id values of the input inside the new, cloned element
        Below are examples of what forms elements you can clone, but not the only ones.
        There are 2 basic structures below: one for an H2, and one for form elements.
        To make more, you can copy the one for form elements and simply update the classes for its label and input.
        Keep in mind that the .val() method is what clears the element when it gets cloned. Radio and checkboxes need .val([]) instead of .val('').
    */
        // H2 - section
        newElem.find('.label_phone').attr('id', 'ID' + newNum + '_reference').attr('name', 'ID' + newNum + '_reference').html('Phone #' + newNum);

        // Phone - text
        newElem.find('.label_phone').attr('for', 'ID' + newNum + '_phone_number');
        newElem.find('.input_phone').attr('id', 'ID' + newNum + '_phone_number').attr('name', 'ID' + newNum + '_phone_number').val('');

    // Insert the new element after the last "duplicatable" input field
        $('#phone' + num).after(newElem);
        $('#ID' + newNum + '_title').focus();

    // Enable the "remove" button. This only shows once you have a duplicated section.
        $('#btnDel_2').attr('disabled', false);

    // Right now you can only add 4 sections, for a total of 5. Change '5' below to the max number of sections you want to allow.
        // This first if statement is for forms using input type="button" (see older demo). DELETE if using button element.
        if (newNum == 5)
        $('#btnAdd_2').attr('disabled', true).prop('value', "You've reached the limit"); // value here updates the text in the 'add' button when the limit is reached
        // This second if statement is for forms using the new button tag (see Bootstrap demo). DELETE if using input type="button" element.
        if (newNum == 5)
        $('#btnAdd_2').attr('disabled', true).text("You've reached the limit"); // value here updates the text in the 'add' button when the limit is reached 
    });

    $('#btnDel_2').click(function () {
    // Confirmation dialog box. Works on all desktop browsers and iPhone.
        if (confirm("Are you sure you wish to remove this phone number? This cannot be undone."))
            {
                var num = $('.clonedInput_2').length;
                // how many "duplicatable" input fields we currently have
                $('#phone' + num).slideUp('slow', function () {$(this).remove();
                // if only one element remains, disable the "remove" button
                    if (num -1 === 1)
                $('#btnDel_2').attr('disabled', true);
                // enable the "add" button. IMPORTANT: only for forms using input type="button" (see older demo). DELETE if using button element.
                $('#btnAdd_2').attr('disabled', false).prop('value', "Add phone");
                // enable the "add" button. IMPORTANT: only for forms using the new button tag (see Bootstrap demo). DELETE if using input type="button" element.
                $('#btnAdd_2').attr('disabled', false).text("Add phone");});
            }
        return false; // Removes the last section you added
    });
    // Enable the "add" button
    $('#btnAdd_2').attr('disabled', false);
    // Disable the "remove" button
    $('#btnDel_2').attr('disabled', true);
});