root = exports ? this

vm = ko.mapping.fromJS({})
vm.report_bases = ko.observableArray()
vm.selected_report_base = ko.observable(0)

vm.reports = ko.observableArray()
vm.selected_report = ko.observable(0)

vm.selected_report_base.subscribe (new_value) ->
	$.ajax
		url: './' + new_value
		success: (data) ->
			vm.reports.removeAll()
			for item in data
				vm.reports.push(ko.mapping.fromJS(item, {}))
	0
	

vm.get_reports = () ->
	$.ajax
		url: './list'
		success: (data) ->
			vm.report_bases.removeAll()
			for item in data
				vm.report_bases.push(ko.mapping.fromJS(item, {}))

	0

vm.display_data = () ->
	nv.addGraph () ->
		chart = nv.models.lineWithFocusChart()

		chart.xAxis.tickFormat (d) ->
			d3.time.format('%d-%m-%Y')(new Date(d))

		chart.x2Axis.tickFormat (d) ->
			d3.time.format('%d-%m-%Y')(new Date(d))

		chart.yAxis.tickFormat(d3.format(',.2f'))
		chart.y2Axis.tickFormat(d3.format(',.2f'))

		data = ko.mapping.toJS(vm.selected_report().plots())
		for plot in data
			for value in plot.values
				value.x = new Date(value.x)

		$('#chart').remove()
		$('#chart-container').append('<svg id="chart"></svg>')
		d3.select('#chart').datum(data).transition().duration(0).call(chart)
		nv.utils.windowResize(chart.update)

	0

root.vm = vm

$ ->
	ko.applyBindings(vm, $('#content')[0])
	vm.get_reports()
