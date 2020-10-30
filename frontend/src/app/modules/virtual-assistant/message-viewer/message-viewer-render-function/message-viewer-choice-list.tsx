import React, { useState } from "react";
import { InboundChoiceList } from "app/common/store/virtual-assistant/types";
import cn from "classnames";

interface MessageViewerChoiceListProps {
	choiceList: InboundChoiceList[];
	sendMessageData: (item: string, renderItem?: string) => () => void;
}

export default function MessageViewerChoiceList(props: MessageViewerChoiceListProps) {
	// Choice list state
	const [isChoiceListVisible, setChoiceListVisibility] = useState<boolean>(true);

	const { choiceList } = props;
	// Choice list auxillary function
	const sendChoiceListData = (message: string) => () => {
		setChoiceListVisibility(false);
		setTimeout(props.sendMessageData(message), 200);
	};

	return (
		<div
			className={cn("message-viewer-choice-list", {
				"message-viewer-choice-list_hidden": !isChoiceListVisible,
			})}
		>
			{choiceList.map((item) => (
				<button
					type="button"
					key={item.title}
					className="message-viewer-choice-list__item"
					onClick={sendChoiceListData(item.title)}
				>
					{item.title}
				</button>
			))}
		</div>
	);
}
