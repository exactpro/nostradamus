import Button, { ButtonStyled } from 'app/common/components/button/button';
import { IconType } from 'app/common/components/icon/icon';
import Field from 'app/modules/filters/field/field';
import { FilterFieldBase } from 'app/modules/filters/field/field-type';
import { FiltersClass } from 'app/modules/filters/filters.class';
import cn from 'classnames';
import React from 'react';
import './filters.scss';

interface InnerProps {
	className?: string;
	filters: FilterFieldBase[],
	applyFilters: (filters: FilterFieldBase[]) => void,
	resetFilters: () => void,
}

export class Filters extends React.Component<InnerProps> {

	filters: FiltersClass;

	constructor(props: InnerProps) {
		super(props);

		this.filters = new FiltersClass(this.props.filters);
	}

	updateField = (field: FilterFieldBase) => {
		this.filters.updateField(field);
		this.forceUpdate();
	}

	resetAll = () => {
		this.filters.resetAllFields();
		this.forceUpdate();
		this.props.resetFilters();
	};

	apply = () => {
		this.props.applyFilters(this.filters.fields);
	};

	checIsFiltersDefault = (filters: FilterFieldBase[]) => filters.reduce((prevVal: boolean, item: FilterFieldBase)=> prevVal && !item.current_value.length, true)

	shouldComponentUpdate = (nextProps: InnerProps) => {

		if(!this.checIsFiltersDefault(this.props.filters) && this.checIsFiltersDefault(nextProps.filters)) this.resetAll();

		return true;
	}

	render() {
		return (
			<div className={cn('filters', this.props.className)}>
				<div className="filters__scroll-container">
					<div className="filters__list">
						{
							this.filters.fields
								.sort((field1, field2) => field1.name > field2.name ? 1 : -1)
								.map((field, index) => (
								<div className="filters__filter" key={index}>
									<div className="filters__filter-name">
										{field.name}
									</div>

									<Field
										className="filters__filter-field"
										field={field}
										updateFunction={this.updateField}
									/>
								</div>
							))
						}
					</div>
				</div>

				<div className="filters__buttons">
					<Button
						styled={ButtonStyled.Flat}
						className="filters__reset-all"
						iconSize={20}
						onClick={this.resetAll}
						text="Clear All" icon={IconType.delete}
					/>

					<Button
						className="filters__apply"
						text="Apply" icon={IconType.check}
						type="submit"
						onClick={this.apply}
						iconSize={28}
					/>
				</div>
			</div>
		);
	}
}
