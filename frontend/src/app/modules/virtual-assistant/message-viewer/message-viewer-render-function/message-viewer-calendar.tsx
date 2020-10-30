import React, { useRef, useEffect, useState } from "react";
import { MessageSendingType } from "app/common/store/virtual-assistant/types";
import Calendar from "react-calendar";
import cn from "classnames";
import Button, { ButtonStyled } from "app/common/components/button/button";
import moment from "moment";

interface MessageViewerCalendarProps {
	calendarTitle: string;
	sendCalendarDate: (item: string, renderItem?: string) => () => void;
}

export default function MessageViewerCalendar(props: MessageViewerCalendarProps) {
	// Calendar variables and state

	const dateRestriction = {
		minDateValue: new Date(0),
		maxDateValue: new Date(),
	};

	const { calendarTitle } = props;

	const dayFormat = ["Su", "Mo", "Tu", "We", "Th", "Fr", "St"];

	const calendarRef = useRef<HTMLDivElement>(null);

	const [calendarValue, setCalendarValue] = useState<undefined | [Date, Date]>(undefined);

	// Calendar auxiliary functions

	const setCalendarDate = (dateVal: Date | [Date, Date]) => {
		let startDate;
		let endDate;

		if (Array.isArray(dateVal)) [startDate, endDate] = dateVal;
		else {
			startDate = new Date(dateVal.getTime());
			endDate = new Date(dateVal.getTime());
		}

		endDate.setHours(23, 59, 59);

		setCalendarValue([startDate, endDate]);
	};

	const sendCalendarDate = () => {
		if (!calendarValue) return;

		const [startDate, endDate] = calendarValue;
		const dateSendMessage: string = JSON.stringify(calendarValue);
		let dateRenderMessage: string;

		if (moment(startDate).isSame(endDate, "day"))
			dateRenderMessage = moment(startDate).format("DD.MM.YYYY");
		else
			dateRenderMessage = `${moment(startDate).format("DD.MM.YYYY")} - ${moment(endDate).format(
				"DD.MM.YYYY"
			)}`;

		props.sendCalendarDate(dateSendMessage, dateRenderMessage)();
		setCalendarValue(undefined);
	};

	// Calendar arrows formatter after render

	useEffect(() => {
		if (!calendarRef.current) return;

		const prevButton = calendarRef.current.getElementsByClassName(
			"react-calendar__navigation__prev-button"
		);
		const nextButton = calendarRef.current.getElementsByClassName(
			"react-calendar__navigation__next-button"
		);

		if (!prevButton || !nextButton) return;

		prevButton[0].classList.add("icon", "icon-Left-Arrow");
		nextButton[0].classList.add("icon", "icon-Left-Arrow", "icon-Left-Arrow__next");

		prevButton[0].innerHTML = "";
		nextButton[0].innerHTML = "";
	});

	return (
		<div
			className={cn(
				"message-viewer-calendar",
				"message-viewer-message",
				`message-viewer-message_${MessageSendingType.inbound}`
			)}
		>
			<p className="message-viewer-calendar__title">{calendarTitle}</p>

			<div ref={calendarRef} className="message-viewer-calendar__calendar">
				<Calendar
					locale="en-EN"
					minDate={dateRestriction.minDateValue}
					maxDate={undefined /* this.dateRestriction.maxDateValue */}
					onClickDay={setCalendarDate}
					onChange={setCalendarDate}
					returnValue="range"
					selectRange
					showNeighboringMonth={false}
					formatShortWeekday={(_: any, date: Date) => dayFormat[date.getDay()]}
				/>
			</div>

			<div
				className={cn("message-viewer-widget-buttons", "message-viewer-widget-buttons_calendar")}
			>
				<Button
					text="Send Date"
					onClick={sendCalendarDate}
					styled={ButtonStyled.Flat}
					type="submit"
					className={cn(
						"message-viewer-widget-buttons__send",
						"message-viewer-widget-buttons__send_shifted"
					)}
				/>
			</div>
		</div>
	);
}
