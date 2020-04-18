$(document).ready(function(){
    $("#myInput").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#myTable tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
    $('input[name="country"]').amsifySuggestags({
        type : 'amsify'
    });
    $('input[name="color"]').amsifySuggestags({
        type : 'amsify',
        suggestions: ['Rash', 'Age', 'Gender', 'Fever', 'Region']
    });
    $('input[name="toAjax"]').amsifySuggestags({
        type : 'amsify',
        suggestionsAction : {
            url : 'jquery-plugins/suggestags/examples/suggestions.php'
        }
    });
    $('input[name="planets"]').amsifySuggestags({
        type : 'amsify',
        suggestions: ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupitor', 'Uranus', 'Neptune', 'Pluto'],
        whiteList: true
    });
    $('input[name="anything"]').amsifySuggestags({
        type : 'amsify',
        tagLimit: 5
    });
    // let myTable = $('#example').DataTable({
    //     "paging": true,
    //     "lengthChange": true,
    //     "searching": true,
    //     "ordering": true,
    //     "info": true,
    //     "autoWidth": true,
    //     "data": [],
    //     "columns": [{
    //             "title": "Arbovírus",
    //             "data": "typeVirus"
    //         }, {
    //             "title": "Nome do Arquivo",
    //             "data": "fileName"
    //         }, {
    //             "title": "Link do Pubmed",
    //             "data": "linkPubmed"
    //         }, {
    //             "title": "Resultado",
    //             "data": "resultado"
    //     }]
    // });
    // $('#bPesquisa').click(function(){
    //     $('.loader').show();
    //     console.log("chegou aqui");
        
    //     let tags = $("#search-tag").val().split(",");
    //     let virus = $("#virus").val();
    //     $('#bPesquisa').prop('disabled', true);
        
    //     $.post('/extract_information/',   // url
    //         { tags, virus }, // data to be submit
    //         function(data, status, jqXHR) {// success callback
    //         myTable.clear();
    //         $.each(data.result, function(index, value) {
    //             myTable.row.add(value);
    //         });
    //         myTable.draw();
    //         $('#bPesquisa').prop('disabled', false);
    //         $('.loader').hide();
    //     });
    // })
    
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});