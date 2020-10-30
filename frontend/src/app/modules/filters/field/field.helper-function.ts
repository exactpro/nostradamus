import {
	FilterFieldDateValue,
	FilterFieldDropdownValue,
	FilterFieldNumberValue,
	FiltrationType,
	ValueUnion,
} from "app/modules/filters/field/field-type";

export const getFieldEmptyValue = (filtration_type: FiltrationType): ValueUnion => {
	switch (filtration_type) {
		case FiltrationType.String:
			return "";

		case FiltrationType.Numeric:
		case FiltrationType.Date:
			return [null, null];

		case FiltrationType.Dropdown:
			return [];
	}
};

export const setFieldValue = (
	filtration_type: FiltrationType,
	newValue: ValueUnion
): ValueUnion => {
	switch (filtration_type) {
		case FiltrationType.String:
			return newValue;

		case FiltrationType.Numeric:
			return [(newValue as FilterFieldNumberValue)[0], (newValue as FilterFieldNumberValue)[1]];

		case FiltrationType.Date:
			const newValueLink = newValue as FilterFieldDateValue;
			const start = newValueLink[0] ? new Date(newValueLink[0]) : null;
			const end = newValueLink[1] ? new Date(newValueLink[1]) : null;
			if (end instanceof Date) {
				end.setHours(23, 59, 59);
			}
			return [start, end];

		case FiltrationType.Dropdown:
			return [...(newValue as FilterFieldDropdownValue)];
	}
};

export const checkFieldIsFilled = (filtration_type: FiltrationType, value: ValueUnion): boolean => {
	switch (filtration_type) {
		case FiltrationType.String:
			return !!value;

		case FiltrationType.Numeric:
		case FiltrationType.Date:
			const valueTyped = value as FilterFieldNumberValue | FilterFieldDateValue;
			return valueTyped.length > 0 && (valueTyped[0] !== null || valueTyped[1] !== null);

		case FiltrationType.Dropdown:
			return !!(value as FilterFieldDropdownValue).length;
	}
};
