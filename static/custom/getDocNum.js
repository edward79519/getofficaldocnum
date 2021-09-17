$(document).ready(function() {
    $(document).on('click', '#getdocnum', function () {
        let id_comp = $('#id_comp :selected').val();
        let id_dept = $('#id_dept :selected').val();
        let date = $('#id_pubdate').val();
        if (id_comp === "" || id_dept === "" || date === "" ){
            $('#msg').text("請選擇公司、部門、時間。")
        } else {
            $.ajax({
                url: '/docnum/ajax/getdocnum',
                method: "GET",
                data: {
                    id_comp: id_comp,
                    id_dept: id_dept,
                    date: date,
                },
                success: function (res) {
                    $('#id_sn').prop('readonly',false);
                    $('#id_sn').val(res.sn);
                    $('#id_sn').prop('readonly',true);
                    $('#id_fullsn').prop('readonly',false);
                    $('#id_fullsn').val(res.full_sn);
                    $('#id_fullsn').prop('readonly',true);
                },
            });
        }
    });
});