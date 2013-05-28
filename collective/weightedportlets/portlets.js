(function($) {
    $(function() {
        $("input.weight").change(function() {
            var pcontainer = $(this).closest("div.managedPortlet"),
                portlethash = pcontainer.attr("data-portlethash"),
                viewname = pcontainer.attr("data-viewname"),
                weight = $(this).val();
                $("<div />").load("@@inlineChangePortletWeight div.portlets-manager > *", {
                    portlethash: portlethash,
                    viewname: viewname,
                    weight: weight})
        })
    });
})(jQuery);
