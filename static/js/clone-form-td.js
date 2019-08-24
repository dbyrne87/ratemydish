/* global $*/
$(function () {
    $('#btnAdd_1').click(function () {
        var num     = $('.clonedInput_1').length, // Checks to see how many "duplicatable" input fields we currently have
            newNum  = new Number(num + 1),      // The numeric ID of the new input field being added, increasing by 1 each time
            newElem = $('#entry' + num).clone().attr('id', 'entry' + newNum).fadeIn('slow'); // create the new element via clone(), and manipulate it's ID using newNum value

        // Label for input_ingredients field
        newElem.find('.ingredients_label').attr('id', 'Field' + newNum + '_reference').attr('name', 'Field' + newNum + '_reference').html('Step #' + newNum);

        // input_ingredients input - text
        newElem.find('.field_ingredients').attr('id', 'Field' + newNum + '_input_ingredients').attr('name', 'Field' + newNum + '_input_ingredients').val=("");

    // Insert the new element after the last "duplicatable" input field
        $('#entry' + num).after(newElem);
        $('input[id=Field' + newNum +'_input_ingredients]').val(''); //Clears the input field of the duplicate field added
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
            newElem = $('#instruction' + num).clone().attr('id', 'instruction' + newNum).fadeIn('slow'); // create the new element via clone(), and manipulate it's ID using newNum value

        // Label for input_instructions field
        newElem.find('.instructions_label').attr('id', 'ID' + newNum + '_reference').attr('name', 'ID' + newNum + '_reference').html('Step #' + newNum);

        // input_instructions input - text
        newElem.find('.field_instructions').attr('id', 'ID' + newNum + '_input_instructions').attr('name', 'ID' + newNum + '_input_instructions').val('');

    // Insert the new element after the last "duplicatable" input field
        $('#instruction' + num).after(newElem);
        $('input[id=Field' + newNum +'_input_instructions]').val(''); //Clears the input field of the duplicate field added
        $('#ID' + newNum + '_title').focus();

    // Enable the "remove" button. This only shows once you have a duplicated section.
        $('#btnDel_2').attr('disabled', false);

        // How many Fields are allowed
        if (newNum == 10)
        $('#btnAdd_2').attr('disabled', true).prop('value', "You've reached the limit"); // value here updates the text in the 'add' button when the limit is reached
    });

    $('#btnDel_2').click(function () {
    // Confirmation dialog box. Works on all desktop browsers and iPhone.
        if (confirm("Are you sure you wish to remove this phone number? This cannot be undone."))
            {
                var num = $('.clonedInput_2').length;
                // how many "duplicatable" input fields we currently have
                $('#instruction' + num).slideUp('slow', function () {$(this).remove();
                // if only one element remains, disable the "remove" button
                    if (num -1 === 1)
                $('#btnDel_2').attr('disabled', true);});
            }
        return false; // Removes the last section you added
    });
    // Enable the "add" button
    $('#btnAdd_2').attr('disabled', false);
    // Disable the "remove" button
    $('#btnDel_2').attr('disabled', true);
});