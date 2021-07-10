import React from "react";
import {
	MessageDataUnion,
	OutboundData,
	InboundData,
} from "app/common/store/virtual-assistant/types";
import cn from "classnames";
import parseMessage from "app/modules/virtual-assistant/message-viewer/message-viewer-render-function/parse-message-function";

interface MessageViewerMessageProps {
	messageItem: MessageDataUnion;
}

export default function MessageViewerMessage(props: MessageViewerMessageProps) {
	const { messageItem } = props;

	const message: string | undefined =
		(messageItem.content as OutboundData).message || (messageItem.content as InboundData).text;
	if (!message) return null;

	const renderMessage = parseMessage([message]);

	return (
		<div
			className={cn("message-viewer-message", `message-viewer-message_${messageItem.messageType}`)}
		>
			{renderMessage}
		</div>
	);
}
