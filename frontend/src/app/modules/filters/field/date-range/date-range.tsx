import Icon, { IconType } from 'app/common/components/icon/icon';
import { FilterFieldBase, FilterFieldDateValue } from 'app/modules/filters/field/field-type';
import { FilterField } from 'app/modules/filters/field/filter-field.class';
import { UpdateFieldFunction } from 'app/modules/filters/filters.class';
import cn from 'classnames';
import React from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import moment from 'moment';
import './date-range.scss';

enum ShowCalendarField{
	startDate="start",
	endDate="end",
}

interface Props {
	className?: string
	field: FilterFieldBase,
	updateFunction: UpdateFieldFunction
}

interface State{
	[key: string]: undefined | ShowCalendarField | string,
	showCalendar: undefined | ShowCalendarField,
	start: undefined | string,
	end: undefined | string,
}

class DateRange extends React.Component<Props, State> {

	field: FilterField;

	state: State = {
		showCalendar: undefined,
		start: undefined,
		end: undefined,
	};

	constructor(props: Props) {
		super(props);

		this.field = new FilterField(this.props.field, this.props.updateFunction)
	}

	editZeroDate = (date: string | Date | undefined): string => {
		if(!date) return "";
		if(date instanceof Date) return [date.getDate(), date.getMonth() + 1, date.getFullYear()].map((item:number, index: number)=> item<10? "0"+item: item).join(".");
		return date.split(".").map((item:string, index: number)=> item.length===1? "0"+item: item).join(".");
	}

	changeVisibleCalendar = (field: ShowCalendarField | undefined = undefined) => () => {
		if(this.state.showCalendar) this.setState({showCalendar: undefined});
		else this.setState({showCalendar: field});
	};

	getDataToUpdate = (field: ShowCalendarField) => {
		if(this.state[field]!==undefined && !this.state[field]!.length) return null
		else{
			let date = moment(this.state[field], ['DD.MM.YY', 'DD.MM.YYYY'], true), defaultDate;
			switch (field) {
				case ShowCalendarField.startDate:
					defaultDate = (this.field.current_value as FilterFieldDateValue)[0]
					break;
				default:
					defaultDate = (this.field.current_value as FilterFieldDateValue)[1]
					break;
			}
			return date.isValid()? date.toDate() : defaultDate
		}
	}

	applyChanges = () => {
		let start = this.getDataToUpdate(ShowCalendarField.startDate),
				end = this.getDataToUpdate(ShowCalendarField.endDate);
		this.field.updateValue([start, end]);
		this.forceUpdate();
		this.field.applyField();
	}

	handleChanges = async (value: Date) => {
		await this.setState({[this.state.showCalendar as ShowCalendarField]: moment(value).format('DD.MM.YYYY'),
									 			  showCalendar: undefined})

		this.applyChanges()
	};

	clearInputField = (field: ShowCalendarField) => async() => {
		await this.setState({[field]:""})
		this.applyChanges()
	}

	handleDirectChanges = (dateField: ShowCalendarField) => (event: React.ChangeEvent<HTMLInputElement>) => {

		this.setState({
			...this.state,
			[dateField]: event.target.value
		});
	};

	onBlurInput = (dateField: ShowCalendarField) =>async () => {
		await this.setState({
			...this.state,
			[dateField]: !this.state[dateField] ||
										moment(this.editZeroDate(this.state[dateField]), ['DD.MM.YY', 'DD.MM.YYYY'], true).isValid()?
										this.editZeroDate(this.state[dateField]):
										'Invalid date'
		});
		this.applyChanges()
	};

	onBlurCalendar = (event: any) => {
		if (!event.currentTarget.contains(event.relatedTarget)) {
			this.changeVisibleCalendar()();
		}
	};

	render() {

		let field  = this.field;
		let value  = this.field.current_value as FilterFieldDateValue;
		let start = value[0], end = value[1];

		let startDate = start ? this.editZeroDate(start): '';
		let endDate = end ? this.editZeroDate(end): '';

		return (
			<div className="date-range" tabIndex={0} onBlur={this.onBlurCalendar}>
				<div className="field date-range__field">
					<input
						type="text"
						className={cn('date-range__input', 'free-input', { 'date-range__input_empty': !start }, this.props.className)}
						name={field.name + '__start'}
						placeholder={this.state.start==="" || this.state.start===undefined? 'Date' : 'Invalid Date'}
						onChange={this.handleDirectChanges(ShowCalendarField.startDate)}
						onBlur={this.onBlurInput(ShowCalendarField.startDate)}
						value={this.state.start===undefined? startDate: this.state.start}
					/>

					<button className="date-range__icon-button_clear"
							 		onClick={this.clearInputField(ShowCalendarField.startDate)}>
						<Icon type={IconType.close} size={16} />
					</button>

					<button className="date-range__icon-button"
									onClick={this.changeVisibleCalendar(ShowCalendarField.startDate)}>
						<Icon type={IconType.calendar} size={16} />
					</button>
				</div>

				<span className="date-range__separator">
					—
				</span>

				<div className="field date-range__field">
					<input
						type="text"
						className={cn('date-range__input', 'free-input', { 'date-range__input_empty': !end }, this.props.className)}
						name={field.name + '__end'}
						placeholder="Date"
						onChange={this.handleDirectChanges(ShowCalendarField.endDate)}
						onBlur={this.onBlurInput(ShowCalendarField.endDate)}
						value={this.state.end || endDate}
					/>

					<button className="date-range__icon-button_clear"
							 		onClick={this.clearInputField(ShowCalendarField.endDate)}>
						<Icon type={IconType.close} size={16} />
					</button>

					<button className="date-range__icon-button"
							 		onClick={this.changeVisibleCalendar(ShowCalendarField.endDate)}>
						<Icon type={IconType.calendar} size={16} />
					</button>
				</div>

				{
					this.state.showCalendar &&
          <Calendar
              locale="en-EN"
              next2Label={false}
              className="date-range__calendar"
							onClickDay={this.handleChanges}
              showNeighboringMonth={false}/>
				}
			</div>
		);
	}
}

export default DateRange;