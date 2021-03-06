// Generated by CoffeeScript 1.9.1
(function() {
  var root, vm;

  root = typeof exports !== "undefined" && exports !== null ? exports : this;

  vm = ko.mapping.fromJS({});

  vm.report_bases = ko.observableArray();

  vm.selected_report_base = ko.observable(0);

  vm.reports = ko.observableArray();

  vm.selected_report = ko.observable(0);

  vm.selected_report_base.subscribe(function(new_value) {
    $.ajax({
      url: './' + new_value,
      success: function(data) {
        var i, item, len, results;
        vm.reports.removeAll();
        results = [];
        for (i = 0, len = data.length; i < len; i++) {
          item = data[i];
          results.push(vm.reports.push(ko.mapping.fromJS(item, {})));
        }
        return results;
      }
    });
    return 0;
  });

  vm.get_reports = function() {
    $.ajax({
      url: './list',
      success: function(data) {
        var i, item, len, results;
        vm.report_bases.removeAll();
        results = [];
        for (i = 0, len = data.length; i < len; i++) {
          item = data[i];
          results.push(vm.report_bases.push(ko.mapping.fromJS(item, {})));
        }
        return results;
      }
    });
    return 0;
  };

  vm.display_data = function() {
    nv.addGraph(function() {
      var chart, data, i, j, len, len1, plot, ref, value;
      chart = nv.models.lineWithFocusChart();
      chart.xAxis.tickFormat(function(d) {
        return d3.time.format('%d-%m-%Y')(new Date(d));
      });
      chart.x2Axis.tickFormat(function(d) {
        return d3.time.format('%d-%m-%Y')(new Date(d));
      });
      chart.yAxis.tickFormat(d3.format(',.2f'));
      chart.y2Axis.tickFormat(d3.format(',.2f'));
      data = ko.mapping.toJS(vm.selected_report().plots());
      for (i = 0, len = data.length; i < len; i++) {
        plot = data[i];
        ref = plot.values;
        for (j = 0, len1 = ref.length; j < len1; j++) {
          value = ref[j];
          value.x = new Date(value.x);
        }
      }
      $('#chart').remove();
      $('#chart-container').append('<svg id="chart"></svg>');
      d3.select('#chart').datum(data).transition().duration(0).call(chart);
      return nv.utils.windowResize(chart.update);
    });
    return 0;
  };

  root.vm = vm;

  $(function() {
    ko.applyBindings(vm, $('#content')[0]);
    return vm.get_reports();
  });

}).call(this);
