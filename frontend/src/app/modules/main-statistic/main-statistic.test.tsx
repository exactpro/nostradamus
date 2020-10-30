/* eslint-disable */
import React from "react";
import { shallow, ShallowWrapper } from "enzyme";
import MainStatistic from "./main-statistic";

describe("Statistic is render counters", () => {
	let wrapper: ShallowWrapper;

	beforeEach(() => {
		wrapper = shallow(<MainStatistic statistic={{ total: 1000, filtered: 500 }} />);
	});

	it("Total block find and contain correct value", () => {
		expect(wrapper.find(".main-statistic__number_type_total").length).toEqual(1);
		expect(wrapper.find(".main-statistic__number_type_total").text()).toEqual("1000");
	});

	it("Filtered block find and contain correct value", () => {
		expect(wrapper.find(".main-statistic__number_type_filtered").length).toEqual(1);
		expect(wrapper.find(".main-statistic__number_type_filtered").text()).toEqual("500");
	});

	it("Have correct custom class", () => {
		wrapper = shallow(<MainStatistic className="test-class" />);
		expect(wrapper.hasClass("test-class")).toEqual(true);
	});

	it("Empty props is correct handled", () => {
		wrapper = shallow(<MainStatistic className="test-class" />);
		expect(wrapper.find(".main-statistic__number_type_total").text()).toEqual("0");
		expect(wrapper.find(".main-statistic__number_type_filtered").text()).toEqual("0");
	});
});
