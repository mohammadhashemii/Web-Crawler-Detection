import {DescriptionContainer, DescriptionText, SampleLog} from "./Elements";

const Description = () => {
    return (
        <>
            <DescriptionContainer>
                <DescriptionText >This is a demo of the <a href="https://rahnemacollege.com/">Rahnema College</a> Machine Learning internship final project. You can upload a log file(e.g. <i>output.log</i>) which contains
                    the server logs in order to detect the crawlers. <a href="https://github.com/mohammadhashemii/Web-Crawler-Detection">[Source Code]</a>
                </DescriptionText>

                <DescriptionText>
                    A sample log is shown here. Therfore, the logs in the file you upload must be the same as the below sample: <a href="https://github.com/mohammadhashemii/Web-Crawler-Detection/blob/master/README.md">[Help]</a>
                </DescriptionText>
                <SampleLog>
                    207.213.193.143 [2021-5-12T5:6:0.0+0430] [Get /cdn/profiles/1026106239] 304 0 [[Googlebot-Image/1.0]] 32
                </SampleLog>
            </DescriptionContainer>
        </>
    );
};

export default Description;