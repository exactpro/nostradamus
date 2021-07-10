import { UpdateFieldFunction } from "app/modules/filters/filters.class";
import cn from "classnames";
import React from "react";

import { FilterFieldBase, FiltrationType } from "app/modules/filters/field/field-type";

import FreeInput from "app/modules/filters/field/free-input/free-input";
import NumericRange from "app/modules/filters/field/numeric-range/numeric-range";
import DateRange from "app/modules/filters/field/date-range/date-range";
import DropDown from "app/modules/filters/field/drop-down/drop-down";

import "app/modules/filters/field/field.scss";

interface Props {
	className?: string;
	field: FilterFieldBase;
	updateFunction: UpdateFieldFunction;
}

class Field extends React.Component<Props> {
	render() {
		const { field } = this.props;
		const { type } = this.props.field;

		return (
			<div className={cn("field-wrapper", this.props.className)}>
				{type === FiltrationType.String && (
					<FreeInput
						className="field__input"
						field={field}
						updateFunction={this.props.updateFunction}
					/>
				)}

				{type === FiltrationType.Dropdown && (
					<DropDown
						className="field__input"
						field={field}
						updateFunction={this.props.updateFunction}
					/>
				)}

				{type === FiltrationType.Numeric && (
					<NumericRange
						className="field__input"
						field={field}
						updateFunction={this.props.updateFunction}
					/>
				)}

				{type === FiltrationType.Date && (
					<DateRange
						className="field__input"
						field={field}
						updateFunction={this.props.updateFunction}
					/>
				)}
			</div>
		);
	}
}

export default Field;
