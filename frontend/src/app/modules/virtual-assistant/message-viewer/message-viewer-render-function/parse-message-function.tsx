import React from "react";
import cn from "classnames";

export default function parseMessage(text: Array<string | React.ReactElement>, parseFunc?: any) {
	if (parseFunc) {
		return text.map((item) => {
			if (typeof item === "string") return parseFunc(item);
			return item;
		});
	}

	return text.map((textItem) => {
		if (typeof textItem === "string") {
			let parsedText: Array<string | React.ReactElement> = [textItem];
			Object.values(parseFunctions).forEach((func) => {
				parsedText = parseMessage(parsedText, func);
			});
			return parsedText;
		}
		return textItem;
	});
}

const parseFunctions = {
	parseUlDash: (text: string) => parseList(text, ListType.dash),
	parseUlPoint: (text: string) => parseList(text, ListType.point),
	parseRef,
};

const ListType = {
	point: {
		isOrdered: false,
		regexSymbol: "*",
		className: "point",
	},
	dash: {
		isOrdered: false,
		regexSymbol: "-",
		className: "dash",
	},
};

function parseList(text: string, listType: typeof ListType[keyof typeof ListType]) {
	const constructList = (startListPosition: number) => {
		return (
			<ul
				className={cn(
					"message-viewer-message__ul",
					`message-viewer-message__ul-${listType.className}`
				)}
				key={startListPosition}
			>
				{parsedText.splice(startListPosition)}
			</ul>
		);
	};

	const listRegex = new RegExp("\\" + listType.regexSymbol + " .*?\n", "g");

	const matchRegex = text.match(listRegex);
	const splitRegex = text.split(listRegex);

	if (!matchRegex) return text;

	const parsedText: Array<string | React.ReactElement> = [];

	let isListOpened = false;
	let startListPosition = 0;

	splitRegex.forEach((item) => {
		if (item) {
			if (isListOpened) {
				isListOpened = false;
				parsedText.push(constructList(startListPosition));
			}

			parsedText.push(...parseMessage([item]));
		}

		if (!isListOpened) {
			startListPosition = parsedText.length;
			isListOpened = true;
		}

		const liContent = matchRegex.shift()?.slice(2, -1);

		if (liContent) {
			parsedText.push(<li key={liContent}>{parseMessage([liContent])}</li>);
		}
	});
	if (isListOpened) {
		parsedText.push(constructList(startListPosition));
	}
	return parsedText;
}

function parseRef(text: string) {
	// the common pattern to render app's link is [link text](link ref), example: [follow the link](http://localhost/)
	const linkRegex = /\[.*?\]\(.*?\)/g;

	const linkArr: any = text.match(linkRegex);

	if (!linkArr) return text;
	// if link is found in message, then divide initial message by the link pattern and render in pairs [text that isn't the link that has been gotten by the division] - [the link]

	const refMessageArr: Array<string | React.ReactNode> = [];
	const textArr: string[] = text.split(linkRegex);

	const linkTextRegex = /[^[]+(?=\])/g;
	const linkRefRegex = /[^(]+(?=\))/g;
	textArr.forEach((item: string, index: number) => {
		let linkText: string | null = null;
		let linkRef: string | null = null;
		const link: any = linkArr[index];
		if (link) {
			linkText = link.match(linkTextRegex)[0];
			linkRef = link.match(linkRefRegex)[0];
		}
		refMessageArr.push(...parseMessage([item]));
		if (linkText && linkRef)
			refMessageArr.push(
				<a
					key={linkText}
					className="message-viewer-message__link-ref"
					href={linkRef}
					target="_blank"
					rel="noopener noreferrer"
				>
					{linkText}
				</a>
			);
	});

	return refMessageArr;
}
