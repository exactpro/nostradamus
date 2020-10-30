import React from "react";
import Icon, { IconSize, IconType } from "app/common/components/icon/icon";
import "app/modules/virtual-assistant/message-input/message-input.scss";

interface MessageInputProps {
	message: string;
	inputMessage: (message: string) => void;
	sendMessage: () => void;
}

export default function MessageInput(props: MessageInputProps) {
	const { message, sendMessage, inputMessage } = props;

	return (
		<div className="message-input">
			<input
				className="message-input__input"
				placeholder="Type a message here"
				value={message}
				onChange={(event) => inputMessage(event.target.value)}
				onKeyPress={(event) => {
					if (event.key === "Enter" && message.length) sendMessage();
				}}
			/>
			<button
				type="button"
				className="message-input__send-button"
				onClick={sendMessage}
				disabled={!message.length}
			>
				<Icon size={IconSize.normal} type={IconType.send} />
			</button>
		</div>
	);
}
