import store from "app/common/store/configureStore";
import { FilterFieldBase, FilterFieldNumberValue } from "app/modules/filters/field/field-type";
import { FilterField } from "app/modules/filters/field/filter-field.class";
import { fixValue } from "app/modules/filters/field/numeric-range/numeric-range.helper-functions";
import ResetValue from "app/modules/filters/field/reset-value/reset-value";
import { UpdateFieldFunction } from "app/modules/filters/filters.class";
import { addToast } from "app/modules/toasts-overlay/store/actions";
import { ToastStyle } from "app/modules/toasts-overlay/store/types";
import cn from "classnames";
import React from "react";

import "./numeric-range.scss";

interface Props {
	className?: string;
	field: FilterFieldBase;
	updateFunction: UpdateFieldFunction;
}

interface State {
	value: string;
}

class NumericRange extends React.Component<Props, State> {
	field: FilterField;

	constructor(props: Props) {
		super(props);

		this.field = new FilterField(this.props.field, this.props.updateFunction);
	}

	handleChanges = (edge: number) => (event: React.ChangeEvent<HTMLInputElement>) => {
		const current_value = this.field.current_value as FilterFieldNumberValue;
		const newValue: FilterFieldNumberValue = [current_value[0], current_value[1]];

		if (isNaN(Number(event.target.value))) {
			store.dispatch(addToast("Unsupported value", ToastStyle.Warning));
		} else {
			newValue[edge] = event.target.value ? Number(event.target.value) : null;
			this.field.updateValue(newValue);
			this.field.applyField();
			this.forceUpdate();
		}
	};

	resetValue = (edge: number) => () => {
		const current_value = this.field.current_value as FilterFieldNumberValue;
		const newValue: FilterFieldNumberValue = [current_value[0], current_value[1]];
		newValue[edge] = null;

		this.field.updateValue(newValue);

		this.forceUpdate();
		this.field.applyField();
	};

	preventIncorrectInputValue = (event: React.KeyboardEvent<HTMLInputElement>) => {
		const allowedValues = "0123456789";
		if (!allowedValues.includes(event.key)) event.preventDefault();
	};

	applyValue = () => {
		const current_value = this.field.current_value as FilterFieldNumberValue;

		this.field.updateValue(fixValue(current_value));
		this.forceUpdate();

		if (current_value[0] || current_value[1]) {
			this.field.applyField();
		}
	};

	render() {
		const { field } = this;
		const current_value = this.field.current_value as FilterFieldNumberValue;

		return (
			<div className="numeric-range">
				<div className="field numeric-range__field">
					<input
						type="text"
						className={cn("numeric-range__input", "free-input", this.props.className)}
						name={`${field.name}__start`}
						value={current_value[0] === null ? "" : current_value[0]}
						onBlur={this.applyValue}
						onChange={this.handleChanges(0)}
						onKeyPress={this.preventIncorrectInputValue}
					/>

					<ResetValue onClick={this.resetValue(0)} className="numeric-range__reset" />
				</div>

				<span className="numeric-range__separator">—</span>

				<div className="field numeric-range__field">
					<input
						type="text"
						className={cn("numeric-range__input", "free-input", this.props.className)}
						name={`${field.name}__end`}
						value={current_value[1] === null ? "" : current_value[1]}
						onBlur={this.applyValue}
						onChange={this.handleChanges(1)}
						onKeyPress={this.preventIncorrectInputValue}
					/>

					<ResetValue onClick={this.resetValue(1)} className="numeric-range__reset" />
				</div>
			</div>
		);
	}
}

export default NumericRange;
