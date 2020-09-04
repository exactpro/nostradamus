import 'app/common/components/card/card.scss';
import CircleSpinner from 'app/common/components/circle-spinner/circle-spinner'; 
import ErrorEmoji from "assets/images/error-emoji.png";
import { isOneOf } from 'app/common/functions/helper';
import { HttpStatus } from 'app/common/types/http.types';
import cn from 'classnames';
import React from 'react'; 

// TODO: refactor to meet solid principles (left only view, remove unnecessary logic)
interface CardProps {
	title?: string;
	className?: string;
	previewImage?: string;
	hoverHeader?: boolean; // for the situation, when we have elements in header of card
	warningMessage: string
	status: HttpStatus;
}
interface CardState{
	hasError: boolean
}

class Card extends React.Component<CardProps, CardState> {

	static defaultProps = {
		status: HttpStatus.FINISHED,
		warningMessage: "Oops! Can't Show You This Card",
	};

	state = {
		hasError: false,
	}

	static getDerivedStateFromError = (): CardState => ({hasError: true});

	render() {

		const { status } = this.props;
		const S = HttpStatus;

		let whenShowPreviewManage = [S.PREVIEW, S.LOADING, S.WARNING, S.FAILED];
		let cardContentStyle: any = {
			backgroundImage: isOneOf(status, whenShowPreviewManage) || this.state.hasError ? `url(${this.props.previewImage})` : 'none',
		}; 

		const errorCondition = status === S.WARNING || status === S.FAILED || this.state.hasError;

		if (errorCondition) {
			cardContentStyle = {
				...cardContentStyle,
				filter: 'blur(3px)'
			};   
		}
		 
		return (
			<section className={cn('card', this.props.className)}>
				{
					this.props.title &&
          <h3 className="card__title" style={{ position: this.props.hoverHeader ? 'absolute' : 'static' }}>
						{this.props.title}
          </h3>
				}

				{
					isOneOf(status, [S.LOADING]) &&
         			<CircleSpinner alignCenter />
				}

				{
					errorCondition &&
					<div className="card-error">
						<img className="card-error__emoji"
							 src={ErrorEmoji}
							 alt="Error Emoji"/>
						<p className="card-error__title">
							{
								this.state.hasError || !this.props.warningMessage.length?
								Card.defaultProps.warningMessage:
								this.props.warningMessage
							}
						</p>
					</div>
				}

				<div className="card__content" style={cardContentStyle}>
					{(status === S.FINISHED && !this.state.hasError) && this.props.children}
				</div>
			</section>
		);
	}
}

export default Card;
