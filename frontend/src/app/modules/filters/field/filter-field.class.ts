import {
	FilterFieldBase,
	FilterFieldDropdownValue,
	FiltrationType,
	ValueUnion,
} from 'app/modules/filters/field/field-type';
import {
	checkFieldIsFilled,
	getFieldEmptyValue,
	setFieldValue,
} from 'app/modules/filters/field/field.helper-function';
import { UpdateFieldFunction } from 'app/modules/filters/filters.class';
import { caseInsensitiveStringCompare } from 'app/common/functions/helper';

export class FilterField {

	// base properties
	name: string;
	filtration_type: FiltrationType;
	exact_match: boolean;
	current_value: ValueUnion;
	values?: FilterFieldDropdownValue;

	// extended properties (don't send to server)
	updateFunction: UpdateFieldFunction;

	constructor(field: FilterFieldBase, updateFunction: UpdateFieldFunction) {
		this.name = field.name;
		this.filtration_type = field.filtration_type;
		this.exact_match = field.exact_match;

		if (field.current_value && checkFieldIsFilled(field.filtration_type, field.current_value)) {
			this.current_value = setFieldValue(field.filtration_type, field.current_value)
		} else {
			this.current_value = setFieldValue(field.filtration_type, getFieldEmptyValue(this.filtration_type));
		}

		if (field.values) {
			this.values = field.values.sort((a,b)=>caseInsensitiveStringCompare(a, b));
		}

		this.updateFunction = updateFunction;
	}

	toggleExactMatch = (exactMatch?: boolean) => {
		this.exact_match = exactMatch === undefined ? !this.exact_match : exactMatch;
		this.applyField();
	};

	updateValue = (newValue: ValueUnion) => {
		this.current_value = setFieldValue(this.filtration_type, newValue);
	};

	resetValue = () => {
		this.toggleExactMatch(false);
		this.updateValue(getFieldEmptyValue(this.filtration_type));
		this.applyField();
	};

	applyField = () => {
		let field: FilterFieldBase= {
			name: this.name,
			filtration_type: this.filtration_type,
			exact_match: this.exact_match,
			current_value: setFieldValue(this.filtration_type, this.current_value),
		}
		if(this.values) field.values=this.values
		this.updateFunction(field)
	};
}
