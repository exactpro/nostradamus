import { FilterFieldNumberValue } from "app/modules/filters/field/field-type";

export const removeLessZero = (value: FilterFieldNumberValue): FilterFieldNumberValue => {
	return [Number(value[0]) < 0 ? 0 : value[0], Number(value[1]) < 0 ? 0 : value[1]];
};

export const switchValue = (value: FilterFieldNumberValue): FilterFieldNumberValue => {
	if (value[0] === null || value[1] === null) {
		return value;
	}

	return [
		Number(value[0]) > Number(value[1]) ? value[1] : value[0],
		Number(value[0]) > Number(value[1]) ? value[0] : value[1],
	];
};

export const fixValue = (value: FilterFieldNumberValue): FilterFieldNumberValue => {
	return removeLessZero(switchValue(value));
};
