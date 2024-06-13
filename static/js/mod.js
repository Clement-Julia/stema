$(document).ready(function() {
    $("body").on("click", ".download_modFiles", function(e) {
        $('.mainFiles').empty();

        const game = $(this).attr("data-game");
        const game_id = $(this).attr("data-gameid");
        const mod_id = $(this).attr("data-modid");
        
        $.ajax({
            type: "GET",
            url: `/mods/files/${game}/${mod_id}/`,
            success: function (data) {
                data = data.files.sort((a, b) => b.uploaded_timestamp - a.uploaded_timestamp);
                data.forEach(function(file) {
                    var section = `
                        <section class="accordion" id="${file.uid}">
                            <h1 class="title">
                                <a href="#${file.uid}">
                                    ${file.name}
                                    <span class="title-info ms-auto">${new Date(file.uploaded_timestamp * 1000).toLocaleDateString('fr-FR', { day: 'numeric', month: 'short', year: 'numeric' })}</span>
                                    <span class="title-info">${file.size_kb > 1000 ? convertSize(file.size_kb) : file.size_kb + "KB"}</span>
                                    <span class="title-upload" data-gameid="${game_id}" data-fileid="${file.file_id}">
                                        <i class="fa-solid fa-lg fa-cloud-arrow-down"></i>
                                    </span>
                                </a>
                            </h1>
                            <div class="content">
                                <div class="wrapper">
                                    <p>
                                        ${file.description}
                                    </p>
                                </div>
                            </div>
                        </section>
                    `;

                    $('.mainFiles').append(section);
                });
            },
            error: function () {
                alert("Une erreur est survenue lors de la récupération des fichiers du mod.");
            }
        });
        $("#modalFiles").modal("show");
    });

    $("body").on("click", ".title-upload", function(e) {
        e.preventDefault();

        const game_id = $(this).attr("data-gameid");
        const file_id = $(this).attr("data-fileid");
        download_modFiles(file_id, game_id);
    });

    function download_modFiles(file_id, game_id) {
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:8000/game_app/mods/proxy/",
            data: {
                fid: file_id,
                game_id: game_id,
            },
            success: function (data) {
                if (data && data.url) {
                    window.location.href = data.url;
                } else {
                    alert("Le mod n'est pas disponible pour le moment.");
                }
            },
            error: function () {
                alert("Une erreur est survenue lors du téléchargement du mod.");
            }
        });
    }

    function convertSize(sizeInKB) {
        const sizeInMB = sizeInKB / 1024;
        return sizeInMB.toFixed(2) + "MB";
    }
});