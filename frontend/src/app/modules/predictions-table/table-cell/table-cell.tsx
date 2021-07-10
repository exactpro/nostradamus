import React, { CSSProperties, useEffect, useRef, useState } from "react";
import cn from "classnames";
import "./table-cell.scss";
import Tooltip from "app/common/components/tooltip/tooltip";

// TODO: refactor method to function
function determineTableCellColor(value: string): string {
	switch (value) {
		case "Won’t Fixed":
			return "green";
		case "Not Won’t Fixed":
			return "dark-blue";

		case "Rejected":
			return "orange";
		case "Not Rejected":
			return "violet-dark";

		case "0–30 days":
			return "cold";
		case "31–90 days":
			return "yellow-strong";
		case "91–180 days":
			return "orange";
		case "> 180 days":
			return "light-red";

		default:
			return "default";
	}
}

function getShortVersion(message: string, length: number) {
	return `${message.slice(0, length)}...`;
}

export default function TableCell({ message }: { message: string }) {
	const [isContentHidden, setIsContentHidden] = useState(false);
	const [isTooltipDisplayed, setIsTooltipDisplayed] = useState(false);
	const tdRef = useRef<HTMLTableDataCellElement>(null);
	const style = useRef<CSSProperties>({});
	const shortenMessageLength = useRef<number | undefined>(undefined);
	useEffect(() => {
		if (tdRef.current) {
			style.current = {
				width: tdRef.current.clientWidth,
			};

			if (tdRef.current.clientWidth < message.replace(/\W/g, "").length * charActualWidth) {
				shortenMessageLength.current = tdRef.current.clientWidth / charActualWidth;
				setIsTooltipDisplayed(true);
			}
		}
	}, [message]);

	const charActualWidth = 10; // Actual average width of symbols with font-size 16px
	const tdMessage =
		isTooltipDisplayed && !isContentHidden && shortenMessageLength.current
			? getShortVersion(message, shortenMessageLength.current)
			: message;
	const tooltipMessage = isContentHidden
		? "Click again to collapse"
		: `${tdMessage}\n\nClick to show whole description`;
	const textColor = determineTableCellColor(message);

	return (
		<td style={style.current} ref={tdRef} className={cn("table-cell", `color_${textColor}`)}>
			{isTooltipDisplayed ? (
				<Tooltip message={tooltipMessage} isDisplayed={isTooltipDisplayed} duration={0}>
					<p className="table-cell__title" onClick={() => setIsContentHidden(!isContentHidden)}>
						{tdMessage}
					</p>
				</Tooltip>
			) : (
				<p className="table-cell__title" onClick={() => setIsContentHidden(!isContentHidden)}>
					{tdMessage}
				</p>
			)}
		</td>
	);
}
