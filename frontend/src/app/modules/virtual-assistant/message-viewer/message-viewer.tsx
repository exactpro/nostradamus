/* eslint-disable react/no-array-index-key */
/* eslint-disable react/jsx-indent-props */
/* eslint-disable react/jsx-indent */
/* eslint-disable no-undef */
import React from "react";
import {
	MessageDataUnion,
	InboundData,
	InboundReport,
	InboundChoiceList,
} from "app/common/store/virtual-assistant/types";
import "app/modules/virtual-assistant/message-viewer/message-viewer.scss";
import chatPicture from "assets/images/chatPicture.png";
import chatbotTypingPreview from "assets/images/chatbotTypingPreview.gif";
import MessageViewerCalendar from "app/modules/virtual-assistant/message-viewer/message-viewer-render-function/message-viewer-calendar";
import MessageViewerDropdownList from "app/modules/virtual-assistant/message-viewer/message-viewer-render-function/message-viewer-dropdown-list";
import MessageViewerFileUpload from "app/modules/virtual-assistant/message-viewer/message-viewer-render-function/message-viewer-file-upload";
import MessageViewerChoiceList from "app/modules/virtual-assistant/message-viewer/message-viewer-render-function/message-viewer-choice-list";
import MessageViewerMessage from "app/modules/virtual-assistant/message-viewer/message-viewer-render-function/message-viewer-message";
import { RootStore } from "app/common/types/store.types";
import { useSelector } from "react-redux";

interface Props {
	messages: MessageDataUnion[];
	selectMessageData: (item: string, renderItem?: string) => () => void;
}

export default function MessageViewer(props: Props) {
	const isTyping = useSelector((state: RootStore) => state.virtualAssistant.typingStatus);
	const { messages, selectMessageData } = props;

	let choiceList: InboundChoiceList[] | undefined;
	let dropdownValues: string[] | undefined;
	let calendarTitle: string | undefined;

	if (messages[0]) {
		choiceList = (messages[0].content as InboundData).buttons;
		if ((messages[0].content as InboundData).custom?.operation === "calendar")
			calendarTitle = (messages[0].content as InboundData).custom?.title;
		if ((messages[0].content as InboundData).custom?.operation === "filtration")
			dropdownValues = (messages[0].content as InboundData).custom?.values;
	}

	return (
		<>
			<div className="message-viewer">
				{calendarTitle && (
					<MessageViewerCalendar
						calendarTitle={calendarTitle}
						sendCalendarDate={selectMessageData}
					/>
				)}

				{dropdownValues && (
					<MessageViewerDropdownList
						allDropdownValues={dropdownValues}
						sendDropdownListData={selectMessageData}
					/>
				)}

				{messages.length ? (
					messages.map((item: MessageDataUnion, index: number) => {
						const report: InboundReport | undefined = (item.content as InboundData).custom;
						if (report?.operation === "report")
							return <MessageViewerFileUpload key={index} report={report} />;
						return <MessageViewerMessage key={index} messageItem={item} />;
					})
				) : (
					<img className="message-viewer__layout-image" src={chatPicture} alt="Robot" />
				)}
			</div>

			{choiceList && (
				<MessageViewerChoiceList choiceList={choiceList} sendMessageData={selectMessageData} />
			)}

			{isTyping && (
				<div className="message-viewer-typing-preview">
					<p className="message-viewer-typing-preview__title">Nostradamus is typing</p>
					<img
						className="message-viewer-typing-preview__image"
						src={chatbotTypingPreview}
						alt="Chatbot typing preview"
					/>
				</div>
			)}
		</>
	);
}
