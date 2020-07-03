import React, {RefObject} from 'react';

import Slider from "app/common/components/slider/slider";

import './frequently-used-terms.scss';

const ONE_ROW_HEIGHT = 29;
const ROW_PER_SLIDE = 4;
const SLIDE_HEIGHT = ONE_ROW_HEIGHT * ROW_PER_SLIDE;

interface FrequentlyUsedTermsState {
  slides: any[]
}

interface FrequentlyUsedTermsProps {
  frequentlyTermsList: string[];
}

class FrequentlyUsedTerms extends React.Component<FrequentlyUsedTermsProps, FrequentlyUsedTermsState> {

  myRef: RefObject<HTMLDivElement>;

  constructor(props: any) {
    super(props);
    this.myRef = React.createRef();
  }

  state = {
    slides: []
  };

  generateSlide = () => {
    if (this.myRef.current) {
      const rowCount = this.myRef.current.offsetHeight / ONE_ROW_HEIGHT;

      let slidesCount: number = Math.ceil(rowCount / ROW_PER_SLIDE);
      let slides: any[] = [];

      for (let i = 0; i < slidesCount; i++) {
        slides.push(this.renderTerms(i)());
      }

      this.setState({
        ...this.state,
        slides
      })
    }
  };

  onResizeWindow = () => {
    this.generateSlide();
  };

  renderTerms = (index: number) => () => {
    let style = {
      marginTop: SLIDE_HEIGHT * index * -1 + 'px'
    };

    return (
      <div className="wrapper" style={style}>
        {
          this.props.frequentlyTermsList.map((word, i) => (
            <div
              className="word"
              key={i}>{word}</div>
          ))
        }
      </div>
    )
  };


  componentDidMount(): void {
    window.addEventListener('resize', this.onResizeWindow);

    if (!this.state.slides.length) {
      this.forceUpdate();
    }
  }

  componentDidUpdate() {
    if (!this.state.slides.length) {
      this.generateSlide();
    }
  }

  componentWillUnmount(): void {
    window.removeEventListener('resize', this.onResizeWindow);
  }

  render() {
    return (
      <React.Fragment>
        <div className="helper">
          <div className="wrapper" ref={this.myRef}>
            {
              this.props.frequentlyTermsList.map((word, i) => (
                <div
                  className="word"
                  key={i}>{word}</div>
              ))
            }
          </div>
        </div>

        <Slider width="100%" height={SLIDE_HEIGHT + 'px'} slides={this.state.slides}/>
      </React.Fragment>
    );
  }
}

export default FrequentlyUsedTerms;
