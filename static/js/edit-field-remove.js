/* global $*/
$(function () {
    
var num = 10;
var num2 = 10;

    $('#btnDel_1').click(function () {
    // Confirmation dialog box. Works on all desktop browsers and iPhone.
        if (confirm("Are you sure you wish to remove this field? This cannot be undone."))
            {

                // how many "duplicatable" input fields we currently have
                $('#entry' + num).slideUp('slow', function () {$(this).remove();
                // if only one element remains, disable the "remove" button
                (num--);    // 1
                if (num === 1)
                $('#btnDel_1').attr('disabled', true);});
            }
        return false; // Removes the last section you added
    });

    $('#btnDel_1').attr('disabled', false);



    $('#btnDel_2').click(function () {
    // Confirmation dialog box. Works on all desktop browsers and iPhone.
        if (confirm("Are you sure you wish to remove this phone number? This cannot be undone."))
            {
                $('#instruction' + num2).slideUp('slow', function () {$(this).remove();
                // if only one element remains, disable the "remove" button
                (num2--);    // 1
                if (num2 === 1)
                $('#btnDel_2').attr('disabled', true);});
            }
        return false; // Removes the last section you added
    });
    // Disable the "remove" button
    $('#btnDel_2').attr('disabled', false);
});